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

HOST = str(sys.argv[1]) # The remote host. Inline Parameter.
PORT = int(sys.argv[2]) # The same port as used by the server. Inline Parameter.

"""<<< TEST LIST COMMAND >>>"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))                               # Connect to a remote socket at address. 
mobile = "0 list"                     				  # String that contains the header and the command
s.sendall(mobile)                                     # Send data to the socket.
data = s.recv(1024)
data = data.split(",")
for i in range (0, len(data)-1):
	res = data[i].split(" ")                                   # Receive data from the server.
	print res[0], res[1]
s.close() 
