"""
HTML Email Templates for MediCareAI
"""
from datetime import datetime

def get_welcome_email_html(user_name: str, user_email: str) -> str:
    """
    Welcome email template for new user signup.
    
    Args:
        user_name: Name of the new user
        user_email: Email of the new user
        
    Returns:
        HTML email content
    """
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background-color: #f0f9ff;
        }}
        .container {{
            background-color: #ffffff;
            margin: 20px;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #0066CC 0%, #06B6D4 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        .logo {{
            width: 60px;
            height: 60px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
            backdrop-filter: blur(10px);
        }}
        .logo-icon {{
            font-size: 32px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        .header p {{
            margin: 8px 0 0 0;
            font-size: 14px;
            color: #E0F2FE;
            opacity: 0.9;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .welcome-badge {{
            background: linear-gradient(135deg, #0066CC 0%, #06B6D4 100%);
            color: white;
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 20px;
        }}
        .greeting {{
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin: 0 0 15px 0;
        }}
        .intro-text {{
            font-size: 16px;
            color: #475569;
            margin-bottom: 25px;
        }}
        .feature-box {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 25px;
            border-radius: 12px;
            margin: 25px 0;
            border-left: 4px solid #0066CC;
        }}
        .feature-box h3 {{
            margin: 0 0 15px 0;
            font-size: 18px;
            color: #0066CC;
            font-weight: 700;
        }}
        .feature-list {{
            margin: 0;
            padding: 0;
            list-style: none;
        }}
        .feature-list li {{
            padding: 10px 0;
            color: #334155;
            font-size: 15px;
            display: flex;
            align-items: center;
        }}
        .feature-list li:before {{
            content: "✓";
            display: inline-block;
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, #0066CC 0%, #06B6D4 100%);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 24px;
            margin-right: 12px;
            font-weight: bold;
            font-size: 14px;
            flex-shrink: 0;
        }}
        .cta-button {{
            display: inline-block;
            padding: 14px 32px;
            background: linear-gradient(135deg, #0066CC 0%, #06B6D4 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
            transition: transform 0.2s;
        }}
        .divider {{
            height: 1px;
            background: linear-gradient(to right, transparent, #e2e8f0, transparent);
            margin: 30px 0;
        }}
        .footer {{
            background: #f8fafc;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
        }}
        .footer-text {{
            font-size: 13px;
            color: #64748b;
            margin: 5px 0;
        }}
        .footer-brand {{
            font-weight: 700;
            background: linear-gradient(135deg, #0066CC 0%, #06B6D4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <span class="logo-icon">❤️</span>
            </div>
            <h1>MediCareAI</h1>
            <p>Your AI-Powered Health Companion</p>
        </div>
        
        <div class="content">
            <div class="welcome-badge">🎉 Welcome Aboard!</div>
            
            <h2 class="greeting">Hello {user_name}!</h2>
            
            <p class="intro-text">
                Thank you for joining <strong>MediCareAI</strong>! We're thrilled to have you as part of our healthcare community. 
                Your account has been successfully created and you're all set to begin your journey to better health.
            </p>
            
            <p class="intro-text">
                <strong>Your registered email:</strong> {user_email}
            </p>
            
            <div class="feature-box">
                <h3>🏥 What You Can Do with MediCareAI</h3>
                <ul class="feature-list">
                    <li>Get AI-powered health insights and symptom analysis</li>
                    <li>Track your medications and health records securely</li>
                    <li>Schedule and manage medical appointments</li>
                    <li>Chat with our AI health assistant 24/7</li>
                    <li>Receive personalized health recommendations</li>
                    <li>Access your complete health dashboard anytime</li>
                </ul>
            </div>
            
            <p class="intro-text">
                Our mission is to make healthcare more accessible, intelligent, and personalized for everyone. 
                We're here to support you every step of the way on your health journey.
            </p>
            
            <div class="divider"></div>
            
            <p class="intro-text">
                If you have any questions or need assistance, our support team is always here to help. 
                Feel free to reach out through our contact form or chat with our AI assistant.
            </p>
            
            <p style="margin-top: 30px; color: #475569;">
                Best regards,<br>
                <strong style="color: #1e293b;">The MediCareAI Team</strong><br>
                <span style="font-size: 14px; color: #64748b;">Empowering Your Health with AI</span>
            </p>
        </div>
        
        <div class="footer">
            <p class="footer-text">
                <span class="footer-brand">MediCareAI</span> - Your AI-Powered Health Companion
            </p>
            <p class="footer-text">
                © 2024 MediCareAI. All rights reserved.
            </p>
            <p class="footer-text">
                This email was sent to {user_email}
            </p>
        </div>
    </div>
</body>
</html>
"""

def get_login_alert_email_html(user_name: str, user_email: str, login_time: str) -> str:
    """
    Login alert email template for security notification.
    
    Args:
        user_name: Name of the user
        user_email: Email of the user
        login_time: Timestamp of the login
        
    Returns:
        HTML email content
    """
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #0066CC 0%, #06B6D4 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            background: #ffffff;
            padding: 30px;
            border: 1px solid #e0e0e0;
        }}
        .alert-icon {{
            font-size: 48px;
            text-align: center;
            margin: 20px 0;
        }}
        .info-box {{
            background: #e0f2fe;
            border-left: 4px solid #0066CC;
            padding: 15px;
            margin: 20px 0;
        }}
        .security-box {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin: 20px 0;
        }}
        .footer {{
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-radius: 0 0 10px 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔐 New Login to Your MediCareAI Account</h1>
    </div>
    
    <div class="content">
        <div class="alert-icon">🔔</div>
        
        <h2>Hello {user_name},</h2>
        
        <p>We detected a new login to your MediCareAI account.</p>
        
        <div class="info-box">
            <h3>📋 Login Details:</h3>
            <p><strong>Email:</strong> {user_email}</p>
            <p><strong>Time:</strong> {login_time}</p>
        </div>
        
        <p><strong>Was this you?</strong></p>
        <p>If you just logged in, you can safely ignore this email. This is just a security notification to keep your account safe.</p>
        
        <div class="security-box">
            <h3>⚠️ If this wasn't you:</h3>
            <p>Someone may have accessed your account. Please take the following steps immediately:</p>
            <ol>
                <li>Change your password</li>
                <li>Contact our support team</li>
                <li>Review your account activity</li>
            </ol>
        </div>
        
        <p>We take your security seriously and will always notify you of account activity.</p>
        
        <p>Best regards,<br>
        <strong>The MediCareAI Security Team</strong></p>
    </div>
    
    <div class="footer">
        <p>© 2024 MediCareAI. All rights reserved.</p>
        <p>This is an automated security notification sent to {user_email}</p>
    </div>
</body>
</html>
"""

def get_welcome_email_subject() -> str:
    """Get subject line for welcome email."""
    return "Welcome to MediCareAI! ❤️ Your Health Journey Begins"

def get_login_alert_subject() -> str:
    """Get subject line for login alert email."""
    return "New Login to Your MediCareAI Account 🔐"

def get_appointment_confirmation_email(user_name: str, doctor_name: str,    specialty: str, 
    appointment_date: str, 
    reason: str,
    meeting_link: str = None
) -> str:
    """
    Appointment confirmation email template.
    
    Args:
        user_name: Name of the patient
        doctor_name: Name of the doctor
        specialty: Doctor's specialty
        appointment_date: Date and time of appointment
        reason: Reason for visit
        meeting_link: Video call link (optional)
        
    Returns:
        HTML email content
    """
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background-color: #f0f9ff;
        }}
        .container {{
            background-color: #ffffff;
            margin: 20px;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #0066CC 0%, #06B6D4 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        .logo {{
            width: 60px;
            height: 60px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
        }}
        .logo-icon {{
            font-size: 32px;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .success-badge {{
            background: #10b981;
            color: white;
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 20px;
        }}
        .appointment-card {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 25px;
            border-radius: 12px;
            margin: 25px 0;
            border-left: 4px solid #0066CC;
        }}
        .appointment-card h3 {{
            margin: 0 0 15px 0;
            font-size: 18px;
            color: #0066CC;
            font-weight: 700;
        }}
        .detail-row {{
            display: flex;
            padding: 10px 0;
            border-bottom: 1px solid #e0f2fe;
        }}
        .detail-row:last-child {{
            border-bottom: none;
        }}
        .detail-label {{
            font-weight: 600;
            color: #475569;
            min-width: 140px;
        }}
        .detail-value {{
            color: #1e293b;
        }}
        .footer {{
            background: #f8fafc;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
        }}
        .footer-text {{
            font-size: 13px;
            color: #64748b;
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <span class="logo-icon">📅</span>
            </div>
            <h1 style="margin: 0; font-size: 28px;">Appointment Confirmed!</h1>
            <p style="margin: 8px 0 0 0; font-size: 14px; color: #E0F2FE;">MediCareAI</p>
        </div>
        
        <div class="content">
            <div class="success-badge">✅ Confirmed</div>
            
            <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
                Hello {user_name},
            </p>
            
            <p style="font-size: 16px; color: #475569; margin-bottom: 25px;">
                Your appointment has been successfully scheduled. Please find the details below:
            </p>
            
            <div class="appointment-card">
                <h3>📋 Appointment Details</h3>
                <div class="detail-row">
                    <div class="detail-label">Doctor:</div>
                    <div class="detail-value">{doctor_name}</div>
                </div>
                <div class="detail-row">
                    <div class="detail-label">Specialty:</div>
                    <div class="detail-value">{specialty}</div>
                </div>
                <div class="detail-row">
                    <div class="detail-label">Date & Time:</div>
                    <div class="detail-value">{appointment_date}</div>
                </div>
                <div class="detail-row">
                    <div class="detail-label">Reason for Visit:</div>
                    <div class="detail-value">{reason}</div>
                </div>
                {f'''
                <div class="detail-row">
                    <div class="detail-label">Video Link:</div>
                    <div class="detail-value"><a href="{meeting_link}" style="color: #0066CC; text-decoration: none; font-weight: bold;">Join Video Call</a></div>
                </div>
                ''' if meeting_link else ''}
            </div>
            
            <p style="font-size: 14px; color: #64748b; margin-top: 25px;">
                <strong>Important Reminders:</strong><br>
                • Please arrive 15 minutes before your scheduled time<br>
                • Bring any relevant medical records or test results<br>
                • If you need to reschedule, please do so at least 24 hours in advance
            </p>
            
            <p style="margin-top: 30px; color: #475569;">
                Best regards,<br>
                <strong style="color: #1e293b;">The MediCareAI Team</strong>
            </p>
        </div>
        
        <div class="footer">
            <p class="footer-text">
                <strong>MediCareAI</strong> - Your AI-Powered Health Companion
            </p>
            <p class="footer-text">
                © 2024 MediCareAI. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>
"""

def get_appointment_cancellation_email(user_name: str, doctor_name: str, appointment_date: str) -> str:
    """Appointment cancellation email template."""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f9ff;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #0066CC 0%, #06B6D4 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2 style="margin: 0;">❌ Appointment Cancelled</h2>
        </div>
        <p>Hello {user_name},</p>
        <p>Your appointment with <strong>{doctor_name}</strong> scheduled for <strong>{appointment_date}</strong> has been cancelled.</p>
        <p>If you would like to reschedule, please log in to your MediCareAI account and book a new appointment.</p>
        <p>Best regards,<br><strong>The MediCareAI Team</strong></p>
    </div>
</body>
</html>
"""

def get_appointment_confirmation_subject() -> str:
    """Get subject line for appointment confirmation email."""
    return "Appointment Confirmed - MediCareAI ✅"

def get_appointment_cancellation_subject() -> str:
    """Get subject line for appointment cancellation email."""
    return "Appointment Cancelled - MediCareAI"
