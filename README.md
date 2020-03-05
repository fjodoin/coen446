# coen446
IoT MQTT project

Clone the project onto your machine and navigate to the /[path-to-project]/coen446/IoT_modules directory

## MUST HAVE Python3 and Pip3 installed on your machine before proceeding ##
Make sure to be in the /IoT_modules directory and install the requirements.txt file before attempting to launch the project; use the following command
terminal#>pip3 install -r requirements.txt

This project emulates a smart home ecosystem with 3 devices connected in a Publisher / Subscriber architecture.

DEVICE 1: MANAGEMENT APPLICATION (management_app.py)	(PUBLISHER)
DEVICE 2: SMART LOCK APPLICATION (smart_lock_app.py)	(PUBLISHER)
DEVICE 3: THERMOMETER APPLICATION (thermometer_app.py)	(SUBSCRIBER)

The BROKER (broker.py) module routes messages via TOPICS; all devices subscribed to a certain topic will receive the same message.

HOW TO LAUNCH PROJECT:
1. Open 4 terminals into the /[path-to-project]/coen446/IoT_modules
2. Launch the broker.py FIRST, if not the connections cannot be established.
terminal1#>python3 broker.py
terminal2#>python3 management_app.py
terminal3#>python3 smart_lock_app.py
terminal4#>python3 thermometer_app.py 
3. Create a user with a preferred temperature with the management_app
4. Enter the username into the smart_lock_app and click "Entering"
5. Notice the temperature change automatically on the thermometer_app
6. All incoming and outgoing messages through the broker is being logged into broker.log

### WARNING ### 
When rebooting the project, you must follow the sequence below in order to avoid socket threading issues. If ever it occurs, simply wait 60seconds before rebooting the broker.
1. close all GUI windows
2. terminate the thermometer listening thread; ctrl+c in terminal4
3. terminate the broker listening thread; ctrl+c x2 in terminal1

TODO:
	Create test cases
