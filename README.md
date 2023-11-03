# envoy_mqtt
Work in Progress 

This is a mqtt publisher app that will request data from a Ensphase Envoy's URL ( older versions example v.02 ) as the recient update from Home Assistance was a breaking change for older devices. 

Dependencies are required:  paho-mqtt and beautifulsoup4

You will need to update your IP address for your local Envoy 

I am currently using the Mosquito MQTT broker and HA core in Docker. 


HA configfuration.yaml
# Template sensor to extract the data from the MQTT JSON object
mqtt:
  - sensor:
      state_topic: "Envoy"
      name: 'Currently'
      unit_of_measurement: 'W'
      value_template: '{{ value_json.Currently }}'

  - sensor:
      state_topic: "Envoy"
      name: 'Today'
      unit_of_measurement: 'Wh'
      value_template: '{{ value_json.Today }}'


To display on the dashboard, create a card using the sensors 'Currently' and 'Today' to display the days power production. 


