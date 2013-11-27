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

# define the function to split the file into smaller chunks
def splitFile(inputFile,noOfChunks):

	#read the contents of the file
	f = open(inputFile, 'rb')
	data = f.read() # read the entire content of the file
	f.close()

	# get the length of data, ie size of the input file in bytes
	bytes = len(data)
	print bytes, noOfChunks

	#calculate the number of chunks to be created
	chunkSize = bytes/(noOfChunks-1)
	if(bytes%(noOfChunks-1) != 0):
		chunkSize+=1

	chunkNames = []
	for i in range(0, bytes+1, chunkSize):
		chunkNames.append(data[i:i+ chunkSize])

	return chunkNames

acum = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))	                              # Sleep for 3 seconds.
mobile = "3 write /hola/cheo.txt"           # String that contains the header and the command
s.sendall(mobile)                                     # Send data to the socket.
data = s.recv(1024)                                   # Receive data from the server.
data = data.split(",")
print data
chunkNames = splitFile("cheo.txt", len(data))
for i in range (0, len(data)-1):
	new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	res = data[i].split(" ")
	print res
	new.connect((HOST, int(res[2]))) #res[1]
	blockInfo = "0//" + str(i) + "//" + chunkNames[i] + "//cheo"
	new.sendall(blockInfo)
	newData = new.recv(1024)	                              # Sleep for 3 seconds.
	print 'Received', repr(newData) 
	new.close()
	acum += res[0] + ":" + str(i) + ","
print 'Received', repr(data)                          # Print recieved success if the connection was succesful.
print "acum: " + acum
s.sendall(acum)
sleep(3)   
s.close() 

acum = ""
"""<<< TEST READ COMMAND >>>"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))								  # Connect to a remote socket at address. 
mobile = "2 read /hola/cheo.txt"                      # String that contains the header and the command
s.sendall(mobile)                                     # Send data to the socket.
data = s.recv(1024)                                   # Receive data from the server.
data = data.split(",")
print data
print "aqui"
i = len(data)-2
while not (i < 0):
	new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	res = data[i].split(" ")
	print "res: " + str(res)
	new.connect((HOST, int(res[2]))) #res[1]
	blockInfo = "1//" + res[3] + "//cheo"
	new.sendall(blockInfo)
	newData = new.recv(1024)                              # Sleep for 3 seconds.
	print 'Received', repr(newData)
	new.close()
	acum += newData
	i -= 1
sleep(3)                                                                                         
s.close()                                             # Close the conection.
print acum
