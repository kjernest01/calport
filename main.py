import imaplib
import email

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def read_credentials():
    with open("credentials.txt", 'r') as file:
        for line in file:
            username, password = line.strip().split(',')  # Assuming the delimiter is a comma
            return {"username": username, "password": password}

# connection to imap server
def connect_to_imap(imap_server, email_address, password):
    # create encrypted connection
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, password)
    return imap

# connection to smtp server
def connect_to_smtp(smtp_server, email_address, password):
    smtp = smtplib.SMTP(smtp_server)
    smtp.starttls() # start secure connection
    smtp.login(email_address, password)
    return smtp

# send email
def send_email(smtp, author, to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = author
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    smtp.sendmail(author, to, msg.as_string())

# check for new emails
def check_for_new_emails(imap, smtp):
    imap.select('inbox')

    result,data = imap.search(None, 'UNSEEN')

    if result == 'OK':
        for num in data[0].split():
            # Fetch the email by its sequence number
            result, email_data = imap.fetch(num, '(RFC822)')
            if result == 'OK':
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)
                # Extract relevant information from the email
                sender = msg['From']
                subject = msg['Subject']
                print(f"New email from {sender}: {subject}")
                content_types = []
                for part in msg.walk():
                    if part.get_content_type() not in content_types:
                        content_types.append(part.get_content_type())
                
                # check for calendar invite
                if "text/calendar" in content_types and "Invitation" in subject:
                    print("this email is a google calendar invite!")
                    # send message back to sender
                    send_email(smtp, read_credentials()['username'], sender, subject, "You sent me an invite. Thanks!")
                else:
                    print("this email is NOT a google calendar invite!")

# main
def main():
    imap_server = "imap.gmail.com"
    smtp_server = "smtp.gmail.com"

    credentials = read_credentials()
    email_address = credentials['username']
    password = credentials['password']

    # Connect to IMAP Server
    imap = connect_to_imap(imap_server, email_address, password)

    # Connect to SMTP Server
    smtp = connect_to_smtp(smtp_server, email_address, password)

    print('Successfully authenticated!')

    try:
        while True:
            try:
                check_for_new_emails(imap, smtp)
            except Exception as e:
                print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print("Listening Stopped.")
        imap.abort()
        smtp.quit()
        pass

if __name__ == "__main__":
    main()