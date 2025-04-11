import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get your GROQ API key from environment



def send_interview_email_rest_api(candidate_name, candidate_email, job_title, interview_date, interview_time, format_type, platform, interviewer_name):
    # Setup API key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")  # Replace with your actual key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Email content
    subject = f"Interview Invitation for {job_title}"
    html_content = f"""
    <html>
    <body>
        <p>Dear {candidate_name},</p>
        <p>Congratulations! You've been shortlisted for the <strong>{job_title}</strong> role.</p>
        <p><strong>📅 Interview Schedule:</strong></p>
        <ul>
            <li><strong>Date:</strong> {interview_date}</li>
            <li><strong>Time:</strong> {interview_time}</li>
            <li><strong>Format:</strong> {format_type}</li>
            <li><strong>Platform:</strong> {platform}</li>
            <li><strong>Interviewer:</strong> {interviewer_name}</li>
        </ul>
        <p>Please confirm your availability by replying to this email.</p>
        <br>
        <p>Best regards,<br>HR Team</p>
    </body>
    </html>
    """

    # Prepare email payload
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": candidate_email}],
        sender={"name": "Recruitment", "email": "vijay.gamer1992@gmail.com"},  # Must be a verified sender in Brevo
        subject=subject,
        html_content=html_content
    )

    # Send email
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("✅ Email sent:", api_response.message_id)
        return True
    except ApiException as e:
        print("❌ Brevo API Exception:", e.body)
        return False
