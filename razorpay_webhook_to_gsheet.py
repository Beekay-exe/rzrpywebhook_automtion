import json
import gspread
from flask import Flask, request
from google.oauth2.service_account import Credentials

# Step 1: Initialize Flask app
app = Flask(__name__)

# Step 2: Setup Google Sheets API credentials
def get_gsheet_client():
    # Define the scope for the Google Sheets API
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    
    # Use the credentials file to authenticate
    creds = Credentials.from_service_account_file('client_secret_623992751201-ngpfn8g8n51qofaek1ge9nqgfj1usgni.apps.googleusercontent.com.json', scopes=SCOPE)
    
    # Authorize the Google Sheets client
    client = gspread.authorize(creds)
    
    return client

# Step 3: Define the webhook route to receive data from Razorpay
@app.route('/webhook', methods=['POST'])
def razorpay_webhook():
    try:
        # Get the webhook data (in JSON format) sent by Razorpay
        webhook_data = request.get_json()

        # Extract relevant fields from the webhook data based on the names provided
        whatsapp_number = webhook_data['payload']['payment']['entity']['notes'].get('Whatsapp Number', 'N/A')
        gender = webhook_data['payload']['payment']['entity']['notes'].get('Gender', 'N/A')
        full_name = webhook_data['payload']['payment']['entity']['notes'].get('Full Name', 'N/A')
        email = webhook_data['payload']['payment']['entity']['notes'].get('Email', 'N/A')
        educational_institution = webhook_data['payload']['payment']['entity']['notes'].get('Educational Institution', 'N/A')
        educational_background = webhook_data['payload']['payment']['entity']['notes'].get('Educational Background', 'N/A')
        district = webhook_data['payload']['payment']['entity']['notes'].get('District', 'N/A')
        date_of_birth = webhook_data['payload']['payment']['entity']['notes'].get('Date Of Birth', 'N/A')
        domain = webhook_data['payload']['payment']['entity']['notes'].get('Choose Your Interested Domain', 'N/A')
        timestamp = webhook_data['payload']['payment']['entity'].get('created_at', 'N/A')

        # Step 4: Convert timestamp to readable format if needed (optional)
        from datetime import datetime
        readable_timestamp = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

        # Step 5: Connect to Google Sheets and add the data
        client = get_gsheet_client()
        sheet = client.open_by_key('1sO6L96-tu3HJYY87-oJ5bCNVjT8iCZ1jYWDoOWNN_oo').worksheet('BasicInfoForm')
        
        # Add the extracted data as a new row in the sheet
        new_row = [readable_timestamp, full_name, email, whatsapp_number, date_of_birth, educational_institution, gender, domain, educational_background, district]
        sheet.append_row(new_row)

        return 'Webhook data received and added to Google Sheets', 200

    except Exception as e:
        print(f"Error: {e}")
        return 'Error processing the webhook', 500

# Step 6: Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
