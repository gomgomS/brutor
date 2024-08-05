import smtplib
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.path.append("../")
sys.path.append("../pytavia_core"    )

from pytavia_core import config

#dont change below the standart
def send() :    
    try:
        # Create the email headers
        my_email= "bersihinyabang@gmail.com"
        ur_pass = "mxfk ezha kgjh sixk"

        with smtplib.SMTP_SSL('smtp.gmail.com',465) as connection:
            connection.login(user=my_email,password=ur_pass)
            connection.sendmail(from_addr=my_email,to_addrs="gomgom223@gmail.com",msg="Subject:apa kabar mas broa")
          
    except Exception as e:
        print(f'Error: {e}')
    return 
# end def

def send_verification_email(params):
    try:
        # Your Gmail credentials
        my_email = "bersihinyabang@gmail.com"
        my_password = "mxfk ezha kgjh sixk"  # Replace with your actual password
        receiver_email = params["email"]  
        # Email content
        subject = "Verification Email Brutaltutor.com"
        body = "Your verification code is: "+params["unique_4_number"]
        sender_name = "BruTor"

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = my_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Attach the body to the email
        message.attach(MIMEText(body, 'plain'))

        # Create SMTP session for sending the mail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(my_email, my_password)
            smtp.sendmail(my_email, receiver_email, message.as_string())
            print("Verification email sent successfully.")
            return True  # Return True if email sent successfully

    except Exception as e:
        print(f'Error sending email: {e}')
        return False  # Return False if there was an error



def attach_send(params):
    to_email   = params["to"       ]
    subject    = params["subject"  ]
    filename   = params["filename" ]
    attachment = params["pdf"      ]
    message    = params["html"     ]

    pdfAttachment = MIMEApplication(attachment, _subtype = 'pdf')
    pdfAttachment.add_header('content-disposition', 'attachment',
        filename=(filename))

    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['To'     ] = to_email
    msg['From'   ] = "bersihinyabang@gmail.com"

    html_email    = MIMEText(message, 'html')
    msg.attach( html_email )
    msg.attach( pdfAttachment )

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login   ("bersihinyabang@gmail.com", "qwertytrewq123")
    server.sendmail("bersihinyabang@gmail.com", to_email , msg.as_string())
    server.quit()
# end def

