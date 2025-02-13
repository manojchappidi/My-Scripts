import subprocess
import pytz
from datetime import datetime
from flask import Flask, jsonify, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'manoj@onwardhealth.co'
app.config['MAIL_PASSWORD'] = 'buwzdtnepfqcezlk'
app.config['MAIL_DEFAULT_SENDER'] = 'manoj@onwardhealth.co'

# Initialize Flask-Mail
mail = Mail(app)

WEBSITES = ['https://aiims.pathflowdx.com/login', 'https://aiimscloud.pathflowdx.com:9001']

def check_websites():
    status = {}
    for website in WEBSITES:
        try:
            response = subprocess.run(["curl", "-I", website], check=True, capture_output=True, text=True, timeout=30)
            status_code = response.stdout.split('\n')[0].split(' ')[1]
            if status_code == '200':
                status[website] = 'UP & Running'
            else:
                status[website] = f'DOWN with Error Code {status_code}'
        except subprocess.CalledProcessError as e:
            status[website] = f"Error: {e}"
        except Exception as e:
            status[website] = f"Error: {e}"
    return status

@app.route('/')
def website_status():
    status = check_websites()
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    return render_template('status.html', status=status, current_time=current_time)

@app.route('/status')
def get_status():
    status = check_websites()

    body = ""
    for website, site_status in status.items():
        body += f"{website}:\n{site_status}\n\n"

        # If the status is an error, include the error message
        if "Error" in site_status:
            body += f"Error Message: {site_status}\n\n"

    # Check if any website is down
    websites_down = [website for website, site_status in status.items() if 'DOWN' in site_status]

    # If any website is down, send an email
    if websites_down:
        recipients = ['manoj@onwardhealth.co', 'manojchappidi999@gmail.com','dinesh@onwardhealth.co','sathish@onwardhealth.co','harshita@onwardhealth.co']  # Add more recipient email addresses here
        msg = Message(subject="Website Down Alert", body=body, recipients=recipients)
        mail.send(msg)

    return jsonify(status)

@app.route('/mail')
def send_mail():
    status = check_websites()

    body = ""
    for website, site_status in status.items():
        body += f"{website}:\n{site_status}\n\n"

        # If the status is an error, include the error message
        if "Error" in site_status:
            body += f"Error Message: {site_status}\n\n"

    recipients = ['manoj@onwardhealth.co', 'manojchappidi999@gmail.com','dinesh@onwardhealth.co','sathish@onwardhealth.co','harshita@onwardhealth.co']  # Add more recipient email addresses here

    msg = Message(subject="Website Status", body=body, recipients=recipients)
    mail.send(msg)

    return jsonify(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)