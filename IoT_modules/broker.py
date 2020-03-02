import socketserver


def create_packet(payload):
    encoded_payload = payload.encode("utf-8")
    encoded_payload_header = f"{len(encoded_payload):<{HEADER_LENGTH}}".encode("utf-8")
    return encoded_payload_header, encoded_payload

HEADER_LENGTH = 10

ecosystem_devices = {}



class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        print("New Connection from: " + self.client_address[0] + ":" + str(self.client_address[1]))
        device_name_header = int(self.request.recv(HEADER_LENGTH).decode("utf-8"))
        device_name = self.request.recv(device_name_header).decode("utf-8")
        print("Device Name: " + device_name)
        if device_name in ecosystem_devices:
            print("Device already connected before!")
            ecosystem_devices[device_name] = self.client_address
        else:
            print("New Device!")
            ecosystem_devices.update({device_name: self.client_address})
            
        for key, value in ecosystem_devices.items():
            print(key, value)

        while True:
            self.data_header_length = int(self.request.recv(HEADER_LENGTH).decode("utf-8"))
            self.data = self.request.recv(self.data_header_length).decode("utf-8")
            print("{} wrote:".format(self.client_address[0] + ":" + str(self.client_address[1])))
            print(self.data)
            
            encoded_payload_header, encoded_payload = create_packet(self.data)
            # just send back the same data, but upper-cased
            self.request.sendall(encoded_payload_header + encoded_payload)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    # Create the server, binding to localhost on port 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
        server.serve_forever()
    print("Server disconnected or terminated!")
    