###############################################################################
#
# Filename: cp.py
#
# Author: 
#			Alex D. Santos Sosa <2013>
#			Ivan Jimenez
#
# Description:
#
#       The main purpose of this script is to handle the copy command
#		issued by the user. When the user runs this script, the script 
#		connects to the meta-data server using the command-line arguments
#		provided by the user. After the connection is stablished the 
#		the meta-data server responds with the data the script requested
#		which is all the available nodes. After the data is received the
#		the scripts parses the data to separate the information of each node
#		and conects to each of them and sends them the chunks of the file. 
#		After the chunks are stored the client sends the meta-data server 
#		the nodes it used to store the chunks.
#
# Run:
#		
#		Pre-requisites - To run this script the meta-data and the data node 
#						 servers must be up and running. See meta-data.py and 
#						 data-node.py.
#
#		- Open terminal
#		- Move to the containing folder
#		- run 'python cp.py < Command > < Path to file in computer > < meta-data server ip > < meta-data server port >:< Path to file in DFS >
#		- i.e. python cp.py -t /Users/Makobi/Documents/hola.txt localhost 30001:Desktop/Test.txt
#		- i.e. python cp.py -f /Users/Makobi/hola.txt localhost 30001:Desktop/Test.txt

# This is how to import a local library
from sock import * # Import local library

#Libraries
import socket              # Library used for the socket functions in this program.
import sys                 # Library used for the inline parameters in this program.
import os 				   # Library used for managing the files	

# define the function to split the file into smaller chunks
def splitFile(inputFile,noOfChunks):

	chunkNames = [] # Stores the chunks

	f = open(inputFile, 'rb') # Open the contents of the file

	data = f.read() # Read the entire content of the file

	f.close() # Close the file

	bytes = len(data) # get the length of data, ie size of the input file in bytes

	chunkSize = bytes/(noOfChunks-1) # Calculate the number of chunks to be created

	if(bytes%(noOfChunks-1) != 0): # Fix ratio
		chunkSize+=1

	for i in range(0, bytes+1, chunkSize): # Split file and store chunks
		chunkNames.append(data[i:i+ chunkSize])

	return chunkNames # Return chunks

HOST = str(sys.argv[3]) # The remote host. Inline Parameter.

port_filepath = str(sys.argv[4]) # Port and DFS path

command = str(sys.argv[1]) # Copy To or From DFS

filepath =  str(sys.argv[2]) # File to be stored to the DFS or file to be stored from DFS

acum = "" # Concatenates the chunks

port_filepath = port_filepath.split(":") # Split the port from the path

PORT = int(port_filepath[0]) # Port

dst = port_filepath[1] # Path to file in the DFS

if command == "-t": # To DFS

	fsize = os.path.getsize(filepath) # Get file size

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.

	s.connect((HOST, PORT))	                              # Sleep for 3 seconds.

	message = "3 write " + str(fsize) + " " + dst        # String that contains the header and the file path on DFS
	
	send_msg(s, message)								# Send data to the socket.

	#s.sendall(message)                                   # Send data to the socket.

	data = recv_msg(s)								 # Receive data from the server.
	
	#data = s.recv(640000000)                             # Receive data from the server.
	
	data = data.split(",")								 # Split the available nodes info from each others
	
	chunkNames = splitFile(filepath, len(data))			 # Split file and get the chunks 
	
	filepath = filepath.split("/")						 # Split filepath
	
	fname = filepath[-1].split(".")						 # Get file name
	
	for i in range (0, len(data)-1): # For each available node

		new = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # New socket to connect to the datanodes

		res = data[i].split(" ") # Separate the attribute of the node
		
		new.connect((str(res[1]), int(res[2]))) # Connect to the Data node
		
		blockInfo = "0//" + str(i) + "//" + chunkNames[i] + "//" + str(fname[0]) # 

		send_msg(new, blockInfo)
		
		#new.sendall(blockInfo) # Send the chunk to the data-node

		newData = recv_msg(new)	# Receive confirmation

		newData = str(newData)
		
		#newData = new.recv(640000000)	  # Receive confirmation

		new.close() # Close socket
		
		acum += res[0] + ":" + str(newData) + "," # Acumulate used nodes
	
	send_msg(s, acum) # Send used nodes to the meta-data server

	#s.sendall(acum) # Send used nodes to the meta-data server
	
	s.close() # Close the socket

elif command == "-f": # From DFS

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.

	s.connect((HOST, PORT))			# Connect to a remote socket at address. 
	
	message = "2 read " + dst       # String that contains the header and the file path on DFS
	
	send_msg(s, message)			# Send data to the socket.

	#s.sendall(message)              # Send message to the socket.

	data = recv_msg(s)				# Receive data-nodes where the file is stored

	data = str(data)
	
	#data = s.recv(640000000)       # Receive data-nodes where the file is stored
	
	data = data.split(",")			# Split the available nodes info from each others
	
	fname = filepath 				# Decided to use the file path as the name
	
	i = 0							# Loop index
	
	while not (i >= (len(data)-1)): # For each data-node

		new = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # New socket to connect to the datanodes
		
		res = data[i].split(" ") # Separate the attribute of the node
		
		new.connect((HOST, int(res[2]))) # Connect to the Data node
		
		blockInfo = "1//" + res[3] + "//" + str(fname[0])

		send_msg(new, blockInfo) # Send the chunk to the data-node
		
		#new.sendall(blockInfo) # Send the chunk to the data-node

		newData = recv_msg(new)	# Receive confirmation
		
		#newData = new.recv(640000000) # Receive confirmation
		
		new.close() # Close socket

		newData = str(newData)
		
		acum += newData # Send used nodes to the meta-data server
		
		i += 1 # Increment counter                                                                                  
	
	s.close() # Close the conection.
	
	complete = str(filepath) # Complete file path
	
	file = open(complete, 'w') # Create file

	file.write(acum) # Write the concatenated chunks into the file

	file.close() # Close file
