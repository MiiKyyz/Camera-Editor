import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import threading




class e_mail():
    User_email = ''
    User_topic = ""
    User_message = ""

    def sender(self):


        self.send_email(self.User_email,
       self.User_topic,
      self.User_message,
       'C:/Users/Mikyo/OneDrive/Escritorio/welcome.jpg')

    def send_email(self,email_recipient,
                   email_subject,
                   email_message,
                   attachment_location = ''):

            email_sender = f"mikyortiz12@hotmail.com"



            msg = MIMEMultipart()
            msg['From'] = email_sender
            msg['To'] = email_recipient
            msg['Subject'] = email_subject

            msg.attach(MIMEText(email_message, 'plain'))

            if attachment_location != '':
                filename = os.path.basename(attachment_location)
                attachment = open(attachment_location, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                "attachment; filename= %s" % filename)
                msg.attach(part)

            try:
                server = smtplib.SMTP('smtp.office365.com', 587)
                server.ehlo()
                server.starttls()
                server.login(email_sender, 'Yankees1224')
                text = msg.as_string()
                server.sendmail(email_sender, email_recipient, text)
                print('email sent')
                server.quit()
            except:
                print("SMPT server connection error")
            return True





