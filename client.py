###############################################################################
#
# File name: client.py

# Authors: Jose R. Ortiz <Year>
#  		  Alex D. Santos Sosa  <2013>
#		  Ivan L. Jimenez Ruiz <2013>
#
# Description:
#       Simple client to test meta-data.py
#


#Libraries

import socket              # Library used for the socket functions in this program.
import sys                 # Library used for the in-line parameters utilized by this program.
from time import sleep     # Library used for the sleep function in this program.

HOST = str(sys.argv[2]) # The remote host. In-line Parameter.
PORT = int(sys.argv[3]) # The same port that the server uses. In-line Parameter.
m_id = str(sys.argv[1]) # The mobile id. In-line Parameter.

"""<<< TEST LIST COMMAND >>>"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))                               # Connect to a remote socket at address. 
mobile = "0 list"                     				  # String that contains the header and the command
s.sendall(mobile)                                     # Send data to the socket.
data = s.recv(1024)                                   # Receive data from the server.
print 'Received', repr(data)                          # Print recieved success if the connection was successful.
sleep(3)     										
s.close() 											  # Close socket connection.

"""<<< TEST WRITE COMMAND >>>"""

# Define the function to split the file into smaller chunks:
def splitFile(inputFile,noOfChunks):

	#chunkNames = [] # Stores the chunks.

	f = open(inputFile, 'rb') # Open the contents of the file.

	data = f.read() # Read the entire content of the file.

	f.close() # Close the file.

	bytes = len(data) # Get the length of data, i.e. size of the input file in bytes.

	chunkSize = bytes/(noOfChunks-1) # Calculate the number of chunks to be created.

	if(bytes%(noOfChunks-1) != 0): # Fix the ratio.
		chunkSize+=1

	for i in range(0, bytes+1, chunkSize): # Split file and store chunks.
		chunkNames.append(data[i:i+ chunkSize])

	return chunkNames # Return chunks.


acum = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))	                              # Connect to a remote socket at address.
mobile = "3 write /hola/cheo.txt"           		  # String that contains the header and the command.
s.sendall(mobile)                                     # Send data to the socket.
data = s.recv(1024)                                   # Receive data from the server.
data = data.split(",") # Split data at every comma.
chunkNames = splitFile("cheo.txt", len(data)) # Use function to split file into chunks.
for i in range (0, len(data)-1):
	new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	res = data[i].split(" ")
	new.connect((HOST, int(res[2]))) #res[1]
	blockInfo = "0//" + str(i) + "//" + chunkNames[i] + "//cheo"
	new.sendall(blockInfo)
	newData = new.recv(1024)	                              
	new.close()
	acum += res[0] + ":" + str(i) + ","
s.sendall(acum)
sleep(3)   # Sleep for 3 seconds.
s.close()  # Close socket connection.

acum = ""
"""<<< TEST READ COMMAND >>>"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))								  # Connect to a remote socket at address. 
mobile = "2 read /hola/cheo.txt"                      # String that contains the header and the command.
s.sendall(mobile)                                     # Send data to the socket.
data = s.recv(1024)                                   # Receive data from the server.
data = data.split(",") # Split data at every comma.
i = len(data)-2
while not (i < 0):
	new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	res = data[i].split(" ")
	new.connect((HOST, int(res[2]))) #res[1]
	blockInfo = "1//" + res[3] + "//cheo"
	new.sendall(blockInfo)
	newData = new.recv(1024)                              
	new.close()
	acum += newData
	i -= 1
sleep(3)                                              # Sleep for 3 seconds.                                          
s.close()                                             # Close socket connection.
