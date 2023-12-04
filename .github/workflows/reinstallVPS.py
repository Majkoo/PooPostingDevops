import ovh
import time
import os
import re

appKey = os.getenv('OVH_APP_KEY')
appSecret = os.getenv('OVH_APP_SECRET')
consKey = os.getenv('OVH_CONSUMER_KEY')

regex = "Debian 12"

client = ovh.Client(
    endpoint='ovh-ca',
    application_key=appKey,
    application_secret=appSecret,
    consumer_key=consKey
)

vpsList = client.get('/vps')
for vps in vpsList:
    nazwa = client.get(f'/vps/{vps}')['displayName']
    if(nazwa == "mgrabka-vps"):
        vpsid = vps
        
imageList = client.get(f'/vps/{vpsid}/images/available')

for image in imageList:
    nazwa = client.get(f'/vps/{vpsid}/images/available/{image}')
    if(re.match(regex, nazwa['name'])):
        imageID = nazwa['id']

client.post(f'/vps/{vpsid}/rebuild/',
                doNotSendPassword=True,
                sshKey="my-key",
                imageId=imageID)

time.sleep(10)
print("Oczekiwanie na reinstalację serwera...")
status = client.get(f'/vps/{vpsid}')['state']
while(status != 'running'):
    time.sleep(5)
    status = client.get(f'/vps/{vpsid}')['state']