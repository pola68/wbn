import smtplib


subject = 'WBN Audit - Miracle Ear'
body = 'This is WBN Audit email.\nHere are results of the latest audit.'
recipients = 'pola68@gmail.com'
gmail_user = 'pola68@gmail.com'
gmail_pwd = ''

smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo(); smtpserver.starttls(); smtpserver.login(gmail_user, gmail_pwd)

header = 'To:' + recipients + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:' + subject + ' \n'
msg = header + '\n' + body + '\n\n'

smtpserver.sendmail(gmail_user, recipients.split(', '), msg)



"""
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.ehlo()
smtp_server.starttls()
smtp_server.login('userEmail', 'pass')

smtp_server.sendmail('mswiader@yodle.com', 'mswiader@yodle.com', 'Subject: Proba od Michala!\nTo jest tylko taki nowy dzien')

smtp_server.quit()
print('Email sent successfully')
"""