from boltiot import Bolt
api_key="ba3f29ed-3a88-44d0-83a5-317f0d6ff54d"
device_id="BOLT14001220"
mybolt = Bolt(api_key, device_id)
response =  response = mybolt.digitalWrite('0', 'LOW')
print (response)


