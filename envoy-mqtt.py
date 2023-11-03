#!/usr/bin/env python3
import time, requests, re, json
import paho.mqtt.client as mqtt
from bs4 import BeautifulSoup

def get_envoy():
    response = requests.get('http://192.168.50.60/production?locale=en')
    soup = BeautifulSoup(response.content, 'html.parser')

    td = soup.find_all('td')
    soup_td_list = list(soup.find_all('td'))

    power_status = {}
    for index, tag in enumerate(soup_td_list):
        if 'Currently' in tag:
            temp = soup_td_list[index + 1].text
            if ' kW' in temp:
                multiplyer = 1000
            if ' W' in temp:
                multiplyer = 1
            power = soup_td_list[index + 1].text.replace(' kWh','').replace(' kW','').replace(' W','')
            power = float(power)
            power = power * multiplyer 

            power_status['Currently'] = power
    for index, tag in enumerate(soup_td_list):
        if 'Today' in tag:
            temp = soup_td_list[index + 1].text
            if ' kWh' in temp:
                multiplyer = 1000
            if ' Wh' in temp:
                multiplyer = 1
            power = soup_td_list[index + 1].text.replace(' kWh','').replace(' Wh','')
            power = float(power)
            power = power * multiplyer 
            power_status['Today'] = power 
    print(power_status)
    power_status = json.dumps(power_status)
    return power_status


def on_publish(client, userdata, mid):
    print("sent a message")


mqttClient = mqtt.Client("envoy")
mqttClient.on_publish = on_publish
mqttClient.connect('192.168.50.50', 1883)
# start a new thread
mqttClient.loop_start()

# Why use msg.encode('utf-8') here
# MQTT is a binary based protocol where the control elements are binary bytes and not text strings.
# Topic names, Client ID, Usernames and Passwords are encoded as stream of bytes using UTF-8.
while True:
    #msg = "hello"
    msg = get_envoy()
    info = mqttClient.publish(
        topic='Envoy',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(300)
