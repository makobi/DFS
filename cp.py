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
import os

# define the function to split the file into smaller chunks
def splitFile(inputFile,noOfChunks):

	#read the contents of the file
	f = open(inputFile, 'rb')
	data = f.read() # read the entire content of the file
	f.close()

	# get the length of data, ie size of the input file in bytes
	bytes = len(data)


	#calculate the number of chunks to be created
	chunkSize = bytes/(noOfChunks-1)
	if(bytes%(noOfChunks-1) != 0):
		chunkSize+=1

	chunkNames = []
	for i in range(0, bytes+1, chunkSize):
		chunkNames.append(data[i:i+ chunkSize])

	return chunkNames

HOST = str(sys.argv[2]) # The remote host. Inline Parameter.
PORT = int(sys.argv[3]) # The same port as used by the server. Inline Parameter.
command = str(sys.argv[1]) # The mobile id. Inline Parameter.
filepath =  str(sys.argv[4])
fsize = os.path.getsize(filepath)
acum = ""

if command == "-t":

	"""<<< TEST WRITE COMMAND >>>"""

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
	s.connect((HOST, PORT))	                              # Sleep for 3 seconds.
	message = "3 write " + str(fsize) + " " + filepath        # String that contains the header and the command
	s.sendall(message)                                     # Send data to the socket.
	data = s.recv(1024)                                   # Receive data from the server.
	data = data.split(",")
	chunkNames = splitFile(filepath, len(data))
	filepath = filepath.split("/")
	fname = filepath[-1].split(".")
	for i in range (0, len(data)-1):
		new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		res = data[i].split(" ")
		print int(res[2])
		new.connect((HOST, int(res[2]))) #res[1]
		blockInfo = "0//" + str(i) + "//" + chunkNames[i] + "//" + str(fname[0])
		new.sendall(blockInfo)
		newData = new.recv(1024)	                              # Sleep for 3 seconds.
		new.close()
		acum += res[0] + ":" + newData + ","
	s.sendall(acum)
	sleep(3)   
	s.close() 

elif command == "-f":

	"""<<< TEST READ COMMAND >>>"""

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
	s.connect((HOST, PORT))								  # Connect to a remote socket at address. 
	message = "2 read " + filepath                      # String that contains the header and the command
	s.sendall(message)                                     # Send data to the socket.
	data = s.recv(1024)                                   # Receive data from the server.
	print data
	print "aqui"
	data = data.split(",")
	filepath = filepath.split("/")
	fname = filepath[-1].split(".")
	i = 0
	print data
	print "aqui 1"
	while not (i >= (len(data)-2)):
		new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		res = data[i].split(" ")
		new.connect((HOST, int(res[2]))) #res[1]
		blockInfo = "1//" + res[3] + "//" + str(fname[0])
		new.sendall(blockInfo)
		newData = new.recv(1024)                              # Sleep for 3 seconds.
		new.close()
		acum += newData
		print acum
		i += 1
	sleep(3)                                                                                         
	s.close()                                             # Close the conection.

print "file: " + acum
