###############################################################################
#
# Filename: list.py
#
# Author: 
#		  
#		Jose R. Ortiz <2012>
#		Alex D. Santos Sosa <2013>
#		Ivan Jimenez
#
# Description:
#
#       The main purpose of this script is to handle the list command
#		issued by the user. When the user runs this script, the script 
#		connects to the meta-data server using the command-line arguments
#		provided by the user. After the connection is stablished the 
#		the meta-data server responds with the data the script requested
#		which is all the files in the DFS. After the data is received the
#		the scripts parses the data to separate the information of each file
#		and prints it.
#
# Run:
#		
#		Pre-requisites - To run this script the meta-data server must be up 
#						 and running. See meta-data.py.
#
#		- Open terminal
#		- Move to the containing folder
#		- run 'python list.py < meta-data server ip > < meta-data server port >
#		- i.e. python meta-data.py localhost 50003
#

#Libraries
import socket              # Library used for the socket functions in this program.
import sys                 # Library used for the inline parameters in this program.

HOST = str(sys.argv[1]) # The remote host. Inline Parameter.
PORT = int(sys.argv[2]) # The same port as used by the server. Inline Parameter.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.

s.connect((HOST, PORT)) # Connect to a remote socket at address. 

message = "0 list" # String that contains the header and the command

s.sendall(message) # Send data to the socket.

data = s.recv(64000) # Receive the meta-data server's answer 								

data = data.split(",") # Split the the data so the files are separeted

for i in range (0, len(data)-1): # For each file

	res = data[i].split(" ")  # Split the file name from the size
	
	print res[0], res[1] # Print the file name and the file size

s.close() # Close the socket
