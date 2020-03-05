import socketserver
import threading
import logging
import json
import datetime
import os

# os.system("python3 smart_lock_app.py")
# os.system("pthyon3 management_app.py")
# os.system("pthyon3 thermometer_app.py")

broker_log_file = 'broker.log'
logging.basicConfig(filename = broker_log_file, filemode = 'a', level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p')

HEADER_LENGTH = 10

ecosystem_devices = {}
connected_users = {}
users_database = {}
topic_dict = {}

service_queue = []
connected_devices_list = []
publisher_list = []
socket_list = []

logging_semaphore = threading.Semaphore()
service_queue_semaphore = threading.Semaphore()



def log_data(tag, data):
    log_dict = {
        "tag": tag,
        "data": data
    }
    log_string = json.dumps(log_dict)
    logging.debug(log_string)


def create_packet(payload):
    encoded_payload = payload.encode("utf-8")
    encoded_payload_header = f"{len(encoded_payload):<{HEADER_LENGTH}}".encode("utf-8")
    return encoded_payload_header, encoded_payload


def broadcast_topic(device_data):
	broadcast_dict = {
		"action": "BROADCAST_TOPIC",
		"publisher": device_data['device'],
		"topic": device_data['publish_topic']
	}
	broadcast_string = json.dumps(broadcast_dict)
	encoded_payload_header, encoded_payload = create_packet(broadcast_string)
	for device in connected_devices_list:
		if device[0] != device_data['device']:
			device[1].sendall(encoded_payload_header + encoded_payload)


class ServiceThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            if len(service_queue) > 0:
                service_queue_semaphore.acquire()
                service_input = service_queue.pop(0)
                service_queue_semaphore.release()
                self.service(service_input)
                logging_semaphore.acquire()
                log_data("Service: ", service_input)
                logging_semaphore.release()

    def service(self, service_input):
        # print(service_input)
        service_input_dict = json.loads(service_input[1])
        device_name = service_input_dict['device']
        if service_input_dict['action'] == "TOPIC_SUBSCRIPTION":
        	self.subscribe_device(service_input_dict)
        elif device_name == "smart_lock":
            self.service_smart_lock(service_input_dict)
        elif device_name == "management_app":
            self.service_management_app(service_input_dict)

    def subscribe_device(self, service_input_dict):
    	for sock in socket_list:
    		if sock[0] == service_input_dict['device']:
    			topic_dict[service_input_dict['topic_of_interest']].append(sock)

	def service_smart_lock(self, service_input_dict):
		if service_input_dict['user'] in users_database:
			topic_notification_dict = {
				"device": service_input_dict['device'],
				"action": "TOPIC_NOTIFICATION",
				"notification": service_input_dict['action']
			}
			topic_notification_string = json.dumps(topic_notification_dict)
			encoded_payload_header, encoded_payload = create_packet
			for subscribed_device in topic_dict['DOOR_STATUS']:
				subscribed_device.sendall(encoded_payload_header + encoded_payload)

		# if service_input_dict['action'] == "ENTERING":
		#     print("ENTERING!")
		#     user = service_input_dict['user']
		#     timestamp = str(datetime.datetime.now())[:19]
		#     # Update list of who is HOME
		#     if user not in connected_users:
		#         connected_users.update({user: timestamp})
		#         print("SET TEMP TO PREF OF USER: " + user)
		#         self.service_thermometer(user, users_database[user])
		#     else:
		#         updated_user = connected_users.pop(user)
		#         connected_users.update({user: timestamp})
		#         print("SET TEMP TO PREF OF USER: " + user)
		#         self.service_thermometer(user, users_database[user])
		# else:
		#     print("LEAVING")
		#     user = service_input_dict['user']
		#     # Update list of who is HOME
		#     if user in connected_users:
		#         current_temp_user = list(connected_users.keys())[len(connected_users)-1]
		#         removed_user = connected_users.pop(user)
		#         if current_temp_user == user:
		#             if len(connected_users) > 0:
		#                 print("SET TEMP TO PREF OF USER: " + list(connected_users.keys())[len(connected_users)-1])
		#                 self.service_thermometer(list(connected_users.keys())[len(connected_users)-1], users_database[list(connected_users.keys())[len(connected_users)-1]])
		#             else:
		#                 print("SET VACANCY TEMP")
		#                 self.service_thermometer("VACANCY", "15")
		# print(connected_users)
		else:
		    print("WARNING: NON-AUTHORIZED USER ATTEMPING TO USE SMART LOCK!")

    def service_management_app(self, service_input_dict):
    	topic_notification_dict = {
			"device": service_input_dict['device'],
			"action": "TOPIC_NOTIFICATION",
			"notification": service_input_dict['action']
        }
        topic_notification_string = json.dumps(topic_notification_dict)
		encoded_payload_header, encoded_payload = create_packet
    	for subscribed_device in topic_dict['USER_MANAGEMENT']:
    		subscribed_device.sendall(encoded_payload_header + encoded_payload)

        # if service_input_dict['action'] == "ADD_NEW_USER":
        #     print("ADD_NEW_USER")
        #     users_database.update({service_input_dict['user_info'][0]: service_input_dict['user_info'][1]})
        # else:
        #     print("DELETE_USER")
        #     deleted_user = users_database.pop(service_input_dict['user_info'][0])
        #     delete_connected_user = connected_users.pop(service_input_dict['user_info'][0])
        #     if len(connected_users) > 0:
        #         print("SET TEMP TO PREF OF USER: " + list(connected_users.keys())[len(connected_users)-1])
        #         self.service_thermometer(list(connected_users.keys())[len(connected_users)-1], users_database[list(connected_users.keys())[len(connected_users)-1]])
        #     else:
        #         print("SET VACANCY TEMP")
        #         self.service_thermometer("VACANCY", "15")
        # print(users_database)

    def service_thermometer(self, user, temperature):
        notification_dict = {
            "device": "broker",
            "user": user,
            "temperature": temperature
        }
        notification_string = json.dumps(notification_dict)
        encoded_payload_header, encoded_payload = create_packet(notification_string)
        thermometer_sock = connected_devices_list[0]
        thermometer_sock.sendall(encoded_payload_header + encoded_payload)
        logging_semaphore.acquire()
        log_data("Notify: ", notification_string)
        logging_semaphore.release()


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # CONNECTION SEQUENCE
        print("Incoming Connection from: " + self.client_address[0] + ":" + str(self.client_address[1]))
        device_data_header = int(self.request.recv(HEADER_LENGTH).decode("utf-8"))
        device_data = self.request.recv(device_data_header).decode("utf-8")
        device_data = json.loads(device_data)
        device_data.update({'device_address': self.client_address})
        # DEVICE WHICH HAS BEEN CONNECTED IN THE PAST
        if device_data['device'] in ecosystem_devices:
            print("Device already connected before!")
            ecosystem_devices[device_data['device']]['device_address'] = self.client_address
            logging_semaphore.acquire()
            log_data("Update Existing Connection", [self.client_address, device_data])
            logging_semaphore.release()
        # NEW DEVICE
        else:
        	connected_devices_list.append([device_name, self.request])
	        if 'publish_topic' in device_data:
	        	topic_dict.update([device_data['publish_topic']: []])
	        	if len(connected_devices_list) > 1:
	        		broadcast_topic(device_data)
        	ecosystem_devices.update({device_name: device_data})
	        logging_semaphore.acquire()
	        log_data("New Connection: ", [self.client_address, device_data])
	        logging_semaphore.release()

	    # LISTENING LOOP
        while True:
            self.data_header_length = int(self.request.recv(HEADER_LENGTH).decode("utf-8"))
            self.data = self.request.recv(self.data_header_length).decode("utf-8")
            input_request = [self.client_address, self.data]
            service_queue_semaphore.acquire()
            service_queue.append(input_request)
            service_queue_semaphore.release()
            logging_semaphore.acquire()
            log_data("Received: ", input_request)
            logging_semaphore.release()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    # Create the server, binding to localhost on port 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
        service_thread = ServiceThread()
        service_thread.start()
        server.serve_forever()
    print("Server disconnected or terminated!")
