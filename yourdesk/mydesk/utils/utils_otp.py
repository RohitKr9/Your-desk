import random
import smtplib
import os

def generateOtp():
    return random.randint(111111,999999)

def sendMail(mail_id):
    email = os.getenv("SENDER_MAIL")
    reciver_mail = mail_id

    subject = "OTP for email verification"
    message = f"Hi this is your otp {generateOtp()}"

    text = f"Subject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    password = os.getenv("MAIL_PASSWORD")
    server.login(email, password)
    server.sendmail(email, reciver_mail, text)
