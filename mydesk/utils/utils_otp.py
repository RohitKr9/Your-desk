import random
import smtplib
import os

def generateOtp():
    return random.randint(111111,999999)

def sendMail(mail_id):
    email = os.getenv("SENDER_MAIL")
    print(email)
    reciver_mail = mail_id

    otp = generateOtp()

    subject = "OTP for email verification"
    message = f"Hi this is your otp {otp}"

    text = f"Subject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    password = os.getenv("MAIL_PASSWORD")
    print(password)
    server.login(email, password)
    print(dir(reciver_mail))
    print(reciver_mail.email)
    server.sendmail(email, [reciver_mail.email], text)
    
    return otp