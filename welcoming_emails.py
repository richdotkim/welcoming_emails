import smtplib
import datetime
import gspread
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from functools import reduce

from .env import SHEET, SENDER, PASSWORD, PORT

def read_email():
    ''' Reads the contents of the email.txt template and returns them as a text variable '''
	with open('email.txt', 'r') as file:
		contents = file.read()
	return contents

def next_weekday(d, weekday):
    ''' Determines the next available date for a given day in the week; Mon = 0, Tue = 1, etc.
        If on day, will return current date. '''
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: #Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)	

# Defining the API's used (needs both feeds and drive for sheets), adding credentials via json file,
#authorizing the clientsheet and getting the instance of the spreadsheet for manipulations
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('json_key.json', scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET)


# Calls the 'Welcoming Team Members' Sheet
members_info_sheet = sheet.get_worksheet(0)
member_info = member_info_sheet.get_all_records()

# Reads the Name and Email Address columns and creates a list of dictionary mappings with names as the keys and email addresses as the values.
# Then takes the list and creates a dictionary of name/ email address = key/value pairs
member_email_list = [{dic['Name']: dic['Email Address']} for dic in member_info]
member_email_dict = {}
for member in member_map:
	result.update(member)

# Calls the 'Welcoming Rotation 2021' Sheet
rotation_info_sheet = sheet.get_worksheet(1)
rotation_info = rotation_info_sheet.get_all_records()

# Creates a dataframe of the welcoming rotation info
rotation_df = pd.DataFrame.from_dict(rotation_info)

next_sunday = next_weekday(datetime.date.today(),6)
next_sunday = next_sunday.strftime('%m/%d/%Y')

# Filters the dataframe for the row for the next available Sunday and removes the date column
sunday_df = rotation_df[rotation_df['Date'] == next_sunday]
sunday_df = sunday_df[['Greeter 1', 'Greeter 2', 'Usher']]

# Gathers the serving members from the filtered row above and creates a list, replacing their names with their emails
# from the member_email_dict created earlier
serving_members = sunday_df.values.tolist()[0]
new_list = [member_email_dict.get(member, member) for member in serving_members]
serving_members_email_list = ','.join(new_list)

# Gmail login account information imported via .env file
sender = SENDER
password = PASSWORD
server = 'smtp.gmail.com'
port = PORT

# Configuration to create SMTP connection and log into SMTP server, create message object,
# and initialize the content for the email body using email.txt
server = smtplib.SMTP_SSL(server, port)
server.login(sender, password)
message = MIMEMultipart()
body = read_email()

# Stating the information for the email and sending it out
message['From'] = SENDER
message['To'] = serving_members_email_list
message['CC'] = CC
message['Subject'] = 'Sunday Service Serving'
message.attach(MIMEText(body, 'plain'))

server.send_message(message)