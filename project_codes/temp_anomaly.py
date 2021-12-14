import email_conf, json, time, math, statistics
from boltiot import Email, Bolt

def compute_bounds(history_data,frame_size,factor):
    if len(history_data)<frame_size :
        return None

    if len(history_data)>frame_size :
        del history_data[0:len(history_data)-frame_size]
    Mn=statistics.mean(history_data)
    Variance=0
    for data in history_data :
        Variance += math.pow((data-Mn),2)
    Zn = factor * math.sqrt(Variance / frame_size)
    High_bound = history_data[frame_size-1]+Zn
    Low_bound = history_data[frame_size-1]-Zn
    return [High_bound,Low_bound]

def send_email(sensor_value):
    mailer = Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_conf.RECIPIENT_EMAIL)
    try:
         print("Making request to Mailgun to send an email")
         response = mailer.send_email("Alert", "The Current temperature sensor value is " +str(sensor_value))
         response_text = json.loads(response.text)
         print("Response received from Mailgun is: " + str(response_text['message']))
    except Exception as e:
        print ("Error occured: Below are the details")
        print (e)


mybolt = Bolt(email_conf.API_KEY, email_conf.DEVICE_ID)
history_data=[]

while True:
    response = mybolt.analogRead('A0')
    data = json.loads(response)
    if data['success'] != 1:
        print("There was an error while retriving the data.")
        print("This is the error:"+data['value'])
        time.sleep(10)
        continue

    print ("This is the value "+data['value'])
    sensor_value=0
    try:
        sensor_value = int(data['value'])
    except Exception as e:
        print("There was an error while parsing the response: ",e)
        continue

    bound = compute_bounds(history_data,email_conf.FRAME_SIZE,email_conf.MUL_FACTOR)
    if not bound:
        required_data_count=email_conf.FRAME_SIZE-len(history_data)
        print("Not enough data to compute Z-score. Need ",required_data_count," more data points")
        history_data.append(int(data['value']))
        time.sleep(10)
        continue

    try:
        if sensor_value > bound[0] :
            print ("Someone has opened the fridge door. Sending an alert..")
            message = "Someone has opened the fridge door."
            telegram_status = send_email(sensor_value)
            print("This is the response ",response)

        history_data.append(sensor_value)
    except Exception as e:
        print ("Error",e)
    time.sleep(10)
