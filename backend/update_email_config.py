#!/usr/bin/env python3
"""
Update .env file with email credentials
"""
from pathlib import Path

# Email credentials
APP_PASSWORD = "obtj kpnu eruq nfdx"
GMAIL_ADDRESS = "vineetkukreti34@gmail.com"  # Based on previous context

# Read current .env
env_path = Path(__file__).parent / ".env"

try:
    with open(env_path, "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("❌ .env file not found!")
    exit(1)

# Update or add email configuration
updated_lines = []
email_config_added = False

for line in lines:
    if line.startswith("SMTP_USER="):
        updated_lines.append(f"SMTP_USER={GMAIL_ADDRESS}\n")
    elif line.startswith("SMTP_PASSWORD="):
        updated_lines.append(f"SMTP_PASSWORD={APP_PASSWORD}\n")
    elif line.startswith("FROM_EMAIL="):
        updated_lines.append(f"FROM_EMAIL={GMAIL_ADDRESS}\n")
    elif line.startswith("FROM_NAME="):
        updated_lines.append(f"FROM_NAME=KisanAI\n")
        email_config_added = True
    else:
        updated_lines.append(line)

# If email config wasn't found, add it
if not email_config_added:
    email_section = f"""
# Email Configuration (Gmail SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER={GMAIL_ADDRESS}
SMTP_PASSWORD={APP_PASSWORD}
FROM_EMAIL={GMAIL_ADDRESS}
FROM_NAME=KisanAI
"""
    updated_lines.append(email_section)

# Write updated .env
with open(env_path, "w") as f:
    f.writelines(updated_lines)

print("✅ Email configuration updated!")
print(f"\n📧 Configuration:")
print(f"   SMTP User: {GMAIL_ADDRESS}")
print(f"   SMTP Password: {APP_PASSWORD[:4]} {APP_PASSWORD[5:9]} {APP_PASSWORD[10:14]} {APP_PASSWORD[15:]}")
print(f"   From Email: {GMAIL_ADDRESS}")
print(f"   From Name: KisanAI")
print("\n🔄 Backend server will auto-reload with new configuration")
print("\n✅ Email notifications are now enabled!")
print("\n📝 Test it:")
print("   1. Create a new account → Receive welcome email")
print("   2. Login → Receive security alert email")
