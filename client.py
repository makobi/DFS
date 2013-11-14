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

HOST = str(sys.argv[2]) # The remote host. Inline Parameter.
PORT = int(sys.argv[3]) # The same port as used by the server. Inline Parameter.
m_id = str(sys.argv[1]) # The mobile id. Inline Parameter.

"""<<< TEST LIST COMMAND >>>"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))                               # Connect to a remote socket at address. 
mobile = "0 list"                     				  # String that contains the header and the command
s.sendall(mobile)                                     # Send data to the socket.
data = s.recv(1024)                                   # Receive data from the server.
print 'Received', repr(data)                          # Print recieved success if the connection was succesful.
sleep(3)     
s.close() 

"""<<< TEST WRITE COMMAND >>>"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))	                              # Sleep for 3 seconds.
mobile = "3 write /hola/cheo.txt n0:1,n1:1"           # String that contains the header and the command
s.sendall(mobile)                                     # Send data to the socket.
data = s.recv(1024)                                   # Receive data from the server.
print 'Received', repr(data)                          # Print recieved success if the connection was succesful.
sleep(3)   
s.close() 

"""<<< TEST READ COMMAND >>>"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))								  # Connect to a remote socket at address. 
mobile = "2 read /hola/cheo.txt"                      # String that contains the header and the command
s.sendall(mobile)                                     # Send data to the socket.
data = s.recv(1024)                                   # Receive data from the server.
print 'Received', repr(data)                          # Print recieved success if the connection was succesful.
sleep(3)                                                                                         
s.close()                                             # Close the conection.
