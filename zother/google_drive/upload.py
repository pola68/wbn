from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Michal Testing.xls'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString("Hello World!\n We'll see to do a little more here") # Set content of the file from given string.
file1.Upload()



# Auto-iterate through all files that matches this query
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
#print(file_list[0][0])
#for file1 in file_list:
#  print('title: %s, id: %s' % (file1['title'], file1['id']))