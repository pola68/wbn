from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


#file1 = drive.CreateFile({'title': 'Michal Testing3333.xls'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
#file1.SetContentString("Hello World!\n We'll see to do a little more here") # Set content of the file from given string.
#file1.Upload()



#file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
#for file1 in file_list:
#  print(file1)
  #print('title: %s, id: %s' % (file1['title'], file1['id']))


  # Paginate file lists by specifying number of max results
for file_list in drive.ListFile({'q': 'trashed=true', 'maxResults': 10}):
  print('Received %s files from Files.list()' % len(file_list)) # <= 10
  for file1 in file_list:
      print('title: %s, id: %s' % (file1['title'], file1['id']))
