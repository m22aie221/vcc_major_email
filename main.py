import functions_framework
import smtplib
from email.mime.text import MIMEText
import os



@functions_framework.http
def send_email(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'

    sender_email = "gcp.serverless.demo@gmail.com"
    app_password = "xxxx xxxx xxxx xxxx"  # App Password, NOT your normal Gmail password
    receiver_email = "m22aie201@iitj.ac.in"

    subject = "📩 Hello from GCP Function (SMTP)"
    body = f"Hi {name},\n\nThis email was sent using Gmail SMTP from GCP Cloud Function."

    # Build email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        # Connect to Gmail SMTP server and send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        return f"✅ Email sent to {receiver_email}!"
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"

    return 'Hello {}!'.format(name)
