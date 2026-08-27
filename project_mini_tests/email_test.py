import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


SENDER_EMAIL=os.getenv("SENDER_EMAIL")
APP_PASSWORD=os.getenv("APP_PASSWORD")



def send_test_email(user: str):

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = user.strip()
    message["Subject"] = "Bankai"

    body_text = "HELLO!! \n \n Go and Watch bleach jare or i will bite you"
    message.attach(MIMEText(body_text, "plain"))

    try:
        print("Connecting to SMTP server...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()  # upgrade connection to secure TLS encryption

            server.login(SENDER_EMAIL, APP_PASSWORD)

            server.sendmail(SENDER_EMAIL, user, message.as_string())
        
       
        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email. Error: {e}")

user = input("Enter your email: ")

send_test_email(user)


