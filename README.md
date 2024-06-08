# calport 
|- an Intelligent Calendar Invite Responder

### An email listener that intelligently responds to Google Calendar Invites

## Setup instructions
1. Enable IMAP by following the below instructions
   1.1 Open Gmail in a web browser
   1.2 Select the Settings gear in the upper-right corner
   1.3 Select "See all settings."
   1.4 Choose the "Forwarding and POP / IMAP" tab
   1.5 In the IMAP access section, select "Enable IMAP."
      1.5a Leave the other settings on the default selections
   1.7 Select "Save Changes."
2. Setup an App Password for your Google Account
   2.2 Go to your Google Account
   2.3 Select Security
   2.4 Under "How you sign in to Google," select 2-Step Verification
   2.5 At the bottom of the page, select App passwords
   2.6 Enter a name that helps you remember where you’ll use the app password
   2.7 Select Generate
   2.8 To enter the app password, follow the instructions on your screen.
      2.8a The app password is the 16-character code that generates on your device.
   2.9 Select Done.
4. Clone this repo
5. Create a "credentials.txt" file with your email and password on the same line separated by a comma and save it to your working directory.
6. Now, run the file by running the following line inside of your working directory on command prompt: ```python main.py```. To exit, please execute 'CTRL+C' from your keyboard

## Version Tracker
version 0.0 - This software is designed to listen to emails (supports only GMAIL for now) and detects if a mail is from Google Calendar or otherwise.
