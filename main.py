import imaplib
import email

def read_credentials():
    with open("credentials.txt", 'r') as file:
        for line in file:
            username, password = line.strip().split(',')  # Assuming the delimiter is a comma
            return {"username": username, "password": password}

# connection to server
def connect_to_imap(imap_server, email_address, password):
    # create encrypted connection
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, password)
    return imap

# check for new emails
def check_for_new_emails(imap):
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
                if "text/calendar" in content_types and "Invitation" in subject:
                    print("this email is a google calendar invite!")
                else:
                    print("this email is NOT a google calendar invite!")

# main
def main():
    imap_server = "imap.gmail.com"
    credentials = read_credentials()
    email_address = credentials['username']
    password = credentials['password']
    
    # Connect to IMAP Server
    imap = connect_to_imap(imap_server, email_address, password)

    print('Successfully authenticated!')

    try:
        while True:
            try:
                check_for_new_emails(imap)
            except Exception as e:
                print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print("Listening Stopped.")
        pass

if __name__ == "__main__":
    main()