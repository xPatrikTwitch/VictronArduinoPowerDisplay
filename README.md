# How to setup?

#1 Connect the graphic 128x64 LCD to your arduino (just google a tutorial and the pinouts), then you can upload the code located in the `Arduino` folder

#2 Set up the VenusOS python program, located in `Venus` folder. You will need to edit the `script_arduino_power_display.py` file and set the `serial_port`, `installation_id`, `api_token` and also the timestamp to set from what date the KWH are counted

Where to get the api token? Go to https://vrm.victronenergy.com/ and then Preferences > Integrations > Access tokens > Add

#3 Run the script by running `python script_arduino_power_display.py` for testing or run the `install.sh` script to run it without needing terminal

_There are  .stl files in the `STL` folder for the 3D printed case i made, there is the bottom part and also Top and TopLED (the led version includes holes for 4x 3mm led if you want to rewire the arduino's TX,RX,PWR,LED leds that are on the pcb_
