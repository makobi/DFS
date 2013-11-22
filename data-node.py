#newpath = r'C:\Program Files\arbitrary' 
#if not os.path.exists(newpath): os.makedirs(newpath)


###############################################################################
#
# Filename: client.py
# Author: Jose R. Ortiz <Year>
#  		  Alex D. Santos Sosa <2013>
#		  Manuel
#		  Ivan Jimenez
#
# Description:
#       Simple client to test meta-data.py
#
#		<<<DESCRIPTION COMING SOON>>>
#

#Libraries
import socket              # Library used for the socket functions in this program.
import sys                 # Library used for the inline parameters in this program.
from time import sleep     # Library used for the sleep function in this program.

HOST = str(sys.argv[1]) # The remote host. Inline Parameter.
PORT = int(sys.argv[2]) # The same port as used by the server. Inline Parameter.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))                               # Connect to a remote socket at address. 

message = "4 true"                     				  # String that contains the header and the command
s.sendall(message)                                     # Send data to the socket.
Nodeid = s.recv(1024)  
print Nodeid
s.close()

