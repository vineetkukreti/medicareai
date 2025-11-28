import xml.etree.ElementTree as ET
from datetime import datetime, date
from typing import Dict, List, Tuple
from collections import defaultdict
import pytz

class AppleHealthParser:
    """Parser for Apple Health export XML files"""
    
    def __init__(self, xml_file_path: str):
        self.xml_file_path = xml_file_path
        self.tree = None
        self.root = None
        
    def parse(self):
        """Parse the XML file"""
        self.tree = ET.parse(self.xml_file_path)
        self.root = self.tree.getroot()
        
    def get_personal_info(self) -> Dict:
        """Extract personal information from <Me> element"""
        me_element = self.root.find('Me')
        if me_element is None:
            return {}
            
        # Parse date of birth
        dob_str = me_element.get('HKCharacteristicTypeIdentifierDateOfBirth')
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
        
        # Parse biological sex
        sex = me_element.get('HKCharacteristicTypeIdentifierBiologicalSex', '')
        if 'Male' in sex:
            biological_sex = 'Male'
        elif 'Female' in sex:
            biological_sex = 'Female'
        else:
            biological_sex = 'Other'
            
        # Parse blood type
        blood_type_raw = me_element.get('HKCharacteristicTypeIdentifierBloodType', '')
        blood_type = blood_type_raw.replace('HKBloodType', '') if blood_type_raw else None
        
        return {
            'date_of_birth': dob,
            'biological_sex': biological_sex,
            'blood_type': blood_type
        }
    
    def get_height_weight(self) -> Tuple[int, int, datetime]:
        """Extract height and weight from records"""
        height = None
        weight = None
        weight_date = None
        
        for record in self.root.findall('Record'):
            record_type = record.get('type')
            
            if record_type == 'HKQuantityTypeIdentifierHeight':
                height_value = record.get('value')
                if height_value:
                    height = int(float(height_value))
                    
            elif record_type == 'HKQuantityTypeIdentifierBodyMass':
                weight_value = record.get('value')
                if weight_value:
                    weight = int(float(weight_value))
                    # Get the date of the weight measurement
                    date_str = record.get('startDate')
                    if date_str:
                        weight_date = self._parse_datetime(date_str)
        
        return height, weight, weight_date
    
    def get_sleep_records(self) -> List[Dict]:
        """Extract sleep analysis records"""
        sleep_sessions = defaultdict(lambda: {
            'start': None,
            'end': None,
            'deep': 0,
            'core': 0,
            'rem': 0
        })
        
        for record in self.root.findall('Record'):
            if record.get('type') == 'HKCategoryTypeIdentifierSleepAnalysis':
                start_str = record.get('startDate')
                end_str = record.get('endDate')
                value = record.get('value')
                
                if not start_str or not end_str:
                    continue
                    
                start_dt = self._parse_datetime(start_str)
                end_dt = self._parse_datetime(end_str)
                
                # Group by date (use the date of sleep end)
                sleep_date = end_dt.date()
                
                # Update session times
                if sleep_sessions[sleep_date]['start'] is None or start_dt < sleep_sessions[sleep_date]['start']:
                    sleep_sessions[sleep_date]['start'] = start_dt
                if sleep_sessions[sleep_date]['end'] is None or end_dt > sleep_sessions[sleep_date]['end']:
                    sleep_sessions[sleep_date]['end'] = end_dt
                
                # Calculate duration in minutes
                duration = int((end_dt - start_dt).total_seconds() / 60)
                
                # Categorize sleep stage based on the category value string
                # Apple Health uses strings like 'HKCategoryValueSleepAnalysisAsleepDeep'
                if value:
                    value_str = value.lower()
                    if 'deep' in value_str or 'asleepdeep' in value_str:
                        sleep_sessions[sleep_date]['deep'] += duration
                    elif 'core' in value_str or 'asleepcore' in value_str:
                        sleep_sessions[sleep_date]['core'] += duration
                    elif 'rem' in value_str or 'asleeprem' in value_str:
                        sleep_sessions[sleep_date]['rem'] += duration
        
        # Convert to list of records
        sleep_records = []
        for sleep_date, data in sleep_sessions.items():
            if data['start'] and data['end']:
                total_duration = int((data['end'] - data['start']).total_seconds() / 60)
                sleep_records.append({
                    'date': sleep_date,
                    'sleep_start': data['start'],
                    'sleep_end': data['end'],
                    'total_duration': total_duration,
                    'deep_sleep': data['deep'],
                    'core_sleep': data['core'],
                    'rem_sleep': data['rem']
                })
        
        return sleep_records
    
    def get_activity_records(self) -> List[Dict]:
        """Extract activity records (steps, distance, calories, flights)"""
        daily_activities = defaultdict(lambda: {
            'steps': 0,
            'distance': 0,
            'flights_climbed': 0,
            'active_calories': 0,
            'basal_calories': 0
        })
        
        for record in self.root.findall('Record'):
            record_type = record.get('type')
            value_str = record.get('value')
            date_str = record.get('startDate')
            
            if not value_str or not date_str:
                continue
            
            # Skip records with non-numeric values (e.g., category type records like sleep analysis)
            try:
                value = float(value_str)
            except ValueError:
                continue
                
            record_date = self._parse_datetime(date_str).date()
            
            if record_type == 'HKQuantityTypeIdentifierStepCount':
                daily_activities[record_date]['steps'] += int(value)
                
            elif record_type == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                # Convert to meters
                unit = record.get('unit')
                if unit == 'km':
                    daily_activities[record_date]['distance'] += int(value * 1000)
                elif unit == 'm':
                    daily_activities[record_date]['distance'] += int(value)
                    
            elif record_type == 'HKQuantityTypeIdentifierFlightsClimbed':
                daily_activities[record_date]['flights_climbed'] += int(value)
                
            elif record_type == 'HKQuantityTypeIdentifierActiveEnergyBurned':
                # Convert to kcal
                unit = record.get('unit')
                if unit == 'kcal':
                    daily_activities[record_date]['active_calories'] += int(value)
                elif unit == 'Cal':
                    daily_activities[record_date]['active_calories'] += int(value)
                    
            elif record_type == 'HKQuantityTypeIdentifierBasalEnergyBurned':
                unit = record.get('unit')
                if unit == 'kcal':
                    daily_activities[record_date]['basal_calories'] += int(value)
                elif unit == 'Cal':
                    daily_activities[record_date]['basal_calories'] += int(value)
        
        # Convert to list
        activity_records = []
        for activity_date, data in daily_activities.items():
            activity_records.append({
                'date': activity_date,
                **data
            })
        
        return activity_records
    
    def get_vital_records(self) -> List[Dict]:
        """Extract vital signs (heart rate, oxygen saturation)"""
        vital_records = []
        
        for record in self.root.findall('Record'):
            record_type = record.get('type')
            value_str = record.get('value')
            date_str = record.get('startDate')
            
            if not value_str or not date_str:
                continue
            
            # Skip records with non-numeric values (e.g., category type records like sleep analysis)
            try:
                value = int(float(value_str))
            except ValueError:
                continue
                
            recorded_at = self._parse_datetime(date_str)
            
            vital_data = {'recorded_at': recorded_at}
            
            if record_type == 'HKQuantityTypeIdentifierHeartRate':
                vital_data['heart_rate'] = value
                vital_records.append(vital_data)
                
            elif record_type == 'HKQuantityTypeIdentifierOxygenSaturation':
                # Convert from decimal to percentage
                vital_data['oxygen_saturation'] = int(value * 100) if value < 1 else value
                vital_records.append(vital_data)
        
        return vital_records
    
    def _parse_datetime(self, date_str: str) -> datetime:
        """Parse datetime string from Apple Health format"""
        # Format: "2025-09-26 20:38:07 +0530"
        try:
            # Remove timezone info and parse
            dt_str = date_str.rsplit(' ', 1)[0]
            dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
            
            # Add timezone info
            # Extract timezone offset
            tz_str = date_str.rsplit(' ', 1)[1]
            if tz_str.startswith('+') or tz_str.startswith('-'):
                # Parse timezone offset
                sign = 1 if tz_str[0] == '+' else -1
                hours = int(tz_str[1:3])
                minutes = int(tz_str[3:5])
                offset_seconds = sign * (hours * 3600 + minutes * 60)
                
                # Create timezone
                tz = pytz.FixedOffset(offset_seconds // 60)
                dt = tz.localize(dt)
            
            return dt
        except Exception as e:
            print(f"Error parsing datetime {date_str}: {e}")
            return datetime.now()
