from __future__ import print_function
import os
import shutil
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)
http = creds.authorize(Http())
DRIVE = build('drive', 'v3', http=creds.authorize(Http()))
MIMETYPE = 'text/plain'
service = build('drive', 'v3', http=http)
results = service.files().list(
    pageSize=1000,fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
memdict={}
memlist=[]
if not items:
    print('No files found.')
else:
    for item in items:
        if ".txt" not in item['name']:
            memlist.append(str(item['name']))
            print( item['name'])
        else:
            memdict.update({str(item['name']):item['id']})
maindir="Member Database"
if not os.path.exists(maindir):
    os.makedirs(maindir)
    os.chdir(maindir)
else:
    os.chdir(maindir)
for i in memdict.keys():
    fileid=memdict[i]
    res=service.files().export(fileId=fileid,mimeType=MIMETYPE).execute()
    if res:
        for j in range(0,len(memlist)):
            if memlist[j] in i:
                dirpath=memlist[j].upper()
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                fn = dirpath+'\%s.txt' % os.path.splitext(i.upper())[0]
                with open(fn,'wb') as fh:
                    fh.write(res)
                with open(fn,'rb') as fh:
                    data=fh.read().decode("utf-8-sig").encode("utf-8")
                with open(fn,'wb') as fh:
                    fh.write(data)
                print('Downloaded "%s"' % (fn))
f=open("Memberlist.txt","w")
for i in memlist:
    f.write(i.upper()+'\n')
f.close()
