import ovh
import time
import os

appKey = os.getenv('OVH_APP_KEY')
appSecret = os.getenv('OVH_APP_SECRET')
consKey = os.getenv('OVH_CONSUMER_KEY')

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

client.post(f'/vps/{vpsid}/rebuild/',
                doNotSendPassword=True,
                sshKey="my-key",
                imageId="Debian 12")

time.sleep(10)