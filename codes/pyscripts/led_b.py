from boltiot import Bolt
api_key="ba3f29ed-3a88-44d0-83a5-317f0d6ff54d"
device_id="BOLT14001220"
mybolt = Bolt(api_key, device_id)
response =mybolt.analogWrite('0', '200')
print (response)


