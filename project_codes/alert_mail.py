import email_conf, json, time
from boltiot import Email, Bolt

minimum_limit = 25 #the minimum threshold of temp value 
maximum_limit = 26.3 #the maximum threshold of temp value 


mybolt = Bolt(email_conf.API_KEY, email_conf.DEVICE_ID)
mailer = Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_conf.RECIPIENT_EMAIL)


while True: 
    print ("Reading sensor value")
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
  # print ("Sensor value is: " + str((data['value'])/10.24))
    try: 
        sensor_value = int(data['value']) *100/1024
        print("Temperature is : "+ str(sensor_value))
        if sensor_value > maximum_limit or sensor_value < minimum_limit:
            print("Making request to Mailgun to send an email")
            response = mailer.send_email("Alert", "The Current temperature sensor value is " +str(sensor_value))
            response_text = json.loads(response.text)
            print("Response received from Mailgun is: " + str(response_text['message']))
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)
