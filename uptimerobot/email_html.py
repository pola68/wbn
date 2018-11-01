#! /usr/bin/python

import smtplib, sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.path.append('/tools')
import mySetup

# me == my email address
# you == recipient's email address
me = "yodlepc@email.com"
you = "mswiader@yodle.com"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <h3>Last 24 hour metrics</h3>
    	<p>
    	All Uptime for 24 hours: <span style="color:red">345</span><br>
    	All Downtime for 24 hours: <span style="color:red">33345</span><br> 
       <p style="color:red">How are you?</p>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.

gmail_user = mySetup.gmailUsername
gmail_pwd = mySetup.gmailPassword
s = smtplib.SMTP("smtp.gmail.com",587)
s.ehlo(); s.starttls(); s.login(gmail_user, gmail_pwd)


# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(me, you, msg.as_string())
s.quit()