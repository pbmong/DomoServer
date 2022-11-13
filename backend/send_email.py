import smtplib
import mimetypes
from email.message import EmailMessage
import sys

SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'pablikco@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'mpupcmovbtlmmpun' #change this to match your gmail app-password

sendTo = 'pablo15monterog@gmail.com'
emailSubject = "DomoServer"
emailContent = sys.argv[1]
attached_file = sys.argv[2]
attached_file_name = attached_file[(attached_file.find("files/")+6):len(attached_file)]

class Emailer:
    def sendmail(self, message):

        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        #Send Email & Exit
        session.send_message(message)
        session.quit

sender = Emailer()
message = EmailMessage()

#sender = "your-name@gmail.com"
#recipient = "example@example.com"
message['From'] = GMAIL_USERNAME
message['To'] = sendTo
message['Subject'] = "DomoServer"
body = emailContent
message.set_content(body)

mime_type, _ = mimetypes.guess_type(attached_file)
mime_type, mime_subtype = mime_type.split('/')
with open(attached_file, 'rb') as file:
 message.add_attachment(file.read(),
 maintype=mime_type,
 subtype=mime_subtype,
 filename=attached_file_name)

#Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
sender.sendmail(message)