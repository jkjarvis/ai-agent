from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64
from datetime import datetime
import pytz

# Sample list of dictionaries with emails to send
emails_to_send = [
    {"email": "anuttamanand@gmail.com", "name": "John Doe", "company": "zerodha", "template": "template1", "schedule": "2024-02-25 17:26:00"},
]

# Sample templates
templates = {
    "template1": """
    {company}'s increased their customer retention rate by 10x.
Do you want the above line to become reality? But thinking how ?
There are only two things which can make it possible: 1) Your product quality, and I'm sure that is one of the best.
2) Your customer support quality. And there I can help.
Presenting AiCare, world's first Ai powered customer support agents to be their with your customers 24x7.
Currently we are focused on 3 objectives:

1. Lowering support costs: train an Ai agent once and deploy any number of times, no more hiring cycles and training sessions for customer support staff, save cost and time.
2. Scaling customer support: something happended and your service went down? Panicked customers are calling but you don’t have the optimal number of support executives to handle? Deploy more Ai agents to handle sudden increase in support calls.
3. Maintaining 24x7 availability: been expanding to different timezones but all your support staff is from the same timezone, bad eh! Keep the Ai agent on call for 24x7, support your customers irrespective of where they live and at what time they call.

Please checkout our website 
You can join our waitlist, we are excited to be working on this new era of innovation and improve how our customers interact with our products and improve their journey.

Thanks
Anuttam

Founder, AiCare""",
}

# Load credentials and create an authorized Gmail API client
creds = Credentials.from_authorized_user_file('token.json')
service = build('gmail', 'v1', credentials=creds)

def create_message_with_schedule(to, subject, message_text, send_at):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {
        'raw': raw,
        'sendAt': send_at,
    }
    return body

def schedule_send_message(service, user_id, body):
    message = (service.users().messages().send(userId=user_id, body=body)
               .execute())
    print(f'Message Id: {message["id"]}')

# Convert schedule string to RFC 3339 format and schedule emails
for email_info in emails_to_send:
    template = templates[email_info['template']]
    message_text = template.format(name=email_info['name'], company=email_info['company'])
    schedule_datetime = datetime.strptime(email_info['schedule'], '%Y-%m-%d %H:%M:%S')
    schedule_rfc3339 = schedule_datetime.astimezone(pytz.utc).isoformat()
    message_body = create_message_with_schedule(email_info['email'], "Scheduled Email", message_text, schedule_rfc3339)
    schedule_send_message(service, 'me', message_body)

