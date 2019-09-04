import docker
from docker import Client
import requests
import json
cli = docker.from_env()
page=1
tags=['master','rocky','stein']
downloads=[]
while(True):
    baseurl=requests.get("https://hub.docker.com/v2/repositories/kolla/?page="+str(page))
    print ("***Fetching info from docker API****\n")
    reqjson=json.loads(baseurl.text)
    if (("detail" in reqjson.keys()) or page==2):
        print ("Page ended")
        break
    results=reqjson['results']
    
    for result in results:
        if ('centos' in result['name']):
            downloads.append(result['name'])
    page=page+1
print (downloads)
total=len(downloads)
for download in downloads:
    print ("*****Found "+download+"*******")
    for tag in tags:
        downloadtag=str(tag)
        downloadpullname=str(download)+":"+str(downloadtag)
        downloadfilename=str(download)+"-"+str(downloadtag)+".tar"
        # print (downloadtag,downloadpullname,downloadfilename)
        try:
            image = cli.pull(downloadpullname)
            print ("********Pulled*******")
            saveimage = cli.get_image(downloadpullname)
            f = open(downloadfilename, 'wb')
            print ("******file opened******")
            for chunk in saveimage:
                f.write(chunk)
            f.close()
            print ("saved")
            total=total-1
            remainingtime= 3*total
            print (str(total)+"**** remaining ****" + " may require"+str(remainingtime)+"mins")
        except Exception as e:
            print ("Exception occured, may be tag not there.", e)
            total=total-1
            remainingtime= 3*total
            print (str(total)+"**** remaining ****" + " may require"+str(remainingtime)+"mins")

