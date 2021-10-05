## Welcoming Email Script ##
**Purpose:**

Our church welcoming team serves off of a rotation for Sunday Service. Sometimes members of the team will forget the day of their rotation and not show up and so the immediate solution was to send out emails in the middle of the week to remind each member who are serving on an upcoming Sunday. This became tedious over time, and so this script was created to automate the reminder/ email sending process using the Google Sheets and Gmail API.

**APIs Used:**
* Google Sheets API
* Google Drive API
* Gmail API

**Additional Files (not already found in repository) required:**
* env.py
* json_key.json

**Welcoming Team Members Sheet example:**
Name  |  Email Address  |  Phone Number  |
-------------  |  -------------  |  -------------  |
John  |  smith.john@gmail.com  |  1234567890
Mary  |  patel.mary@gmail.com  |  0987654321
Bob   |  green.bob@gmail.com   |  4561237890

**Welcoming Rotation Sheet example:**
Date  | Greeter 1  |  Greeter 2  | Usher
------------- | -------------  |  -------------  |  -------------  |
20211003  | John  |  Mary  |  Steve  |
20211010 |  Victoria  |  Bob  |  Gerald  |
