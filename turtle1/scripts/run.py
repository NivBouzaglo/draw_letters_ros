#!/usr/bin/env python3

import time
from subprocess import Popen



server = Popen(["rosrun", "turtle1", "service_server_node.py"])
print_server = Popen(["rosrun", "turtle1", "subscriber_node.py"])
client = Popen("""rosrun turtle1 client_service_server_node.py 3 1 'L' 'yellow'""",shell =True)
client.wait()
client1 = Popen("""rosrun turtle1 client_service_server_node.py 6 1 'I' 'black'""",shell=True)
client1.wait()
client2 = Popen("""rosrun turtle1 client_service_server_node.py 9 1 'T' 'yellow'""",shell=True)
client2.wait()

printer = Popen(["rosservice", "call", "/printer"])
printer.wait()
printer.terminate()
