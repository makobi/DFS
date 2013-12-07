
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
#       The main purpose of this script is to create a datanode that stores
#		the chunks sent by the client. When the user runs this script it sends
#		a mesage to the meta-data indicating that it is alive and creates a
#		a directory to store the chunks in. When it receives a write command
# 		it creates a file for the chunk and stores it. If it receive a copy to
#		DFS it reads the chunk and send it to the client.
#
# Run:
#		
#		Pre-requisites - To run this script the meta-data server must be up 
#						 and running. See meta-data.py.
#
#		- Open terminal
#		- Move to the containing folder
#		- run 'python data-node.py < meta-data server ip > < meta-data server port > < data-node id number > < data-node ip > < data-node port >
#		- i.e. python meta-data.py localhost 50003 1 localhost 50001

#Libraries
import socket          # Library used for the socket functions in this program.
import threading       # Library used for the threads and its functions in the program.
import sys             # Library used for the inline parameters in this program.


# Handle Class Thread
class Handle_thread (threading.Thread):

	# Initialization of the thread
	def __init__(self, name, conn, addr):
		threading.Thread.__init__(self)
		self.name = name
		self.conn = conn
		self.addr = addr
		print "Starting " + self.name

	# Define what the thread is to do
	def run(self):
		""" This thread will listen to the client messages from client.py and then print 
			the command the client wants to execute"""

		global ChunkIdCount # Id for chunks

		data = conn.recv(640000000)  # Receives a message from the client

		info = data.split("//") # Split the message

		if data[0] == str(0): # If copy to

			file = open("n" + str(Nodeid)  + "/_bk" + str(ChunkIdCount) + '.dat', 'w') # Create file in node directory

			file.write(str(info[2])) # Write the chunk into the file

			file.close() # Close the file

			conn.sendall(str(ChunkIdCount)) # Send chunk id

			ChunkIdCount += 1 # Increment chunk id

		elif data[0] == str(1): # If copy from

			f = open("n" + str(Nodeid) + "/_bk" + str(info[1]) + '.dat', 'rb') # Open fie of chunk to read

			Chunk = f.read() # read the entire content of the file

			f.close() # close file

			conn.sendall(Chunk) # Send chunk

		conn.close()            # Close the connection.

#Libraries
import socket              # Library used for the socket functions in this program.
import sys                 # Library used for the inline parameters in this program.
import os				   # Library used for making directories

HOST = str(sys.argv[1]) # The remote host. Inline Parameter.

PORT = int(sys.argv[2]) # The same port as used by the server. Inline Parameter.

Nodeid = int(sys.argv[3]) # Node id

Nodeip = str(sys.argv[4]) # Node IP address

Nodeport = int(sys.argv[5]) # Node port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.

s.connect((HOST, PORT))                               # Connect to a remote socket at address. 

max_threads = 5 # Maximum Threads allowed

ChunkIdCount = 0 # Initialize chunk id counter

threads = []*max_threads # Store threads

message = "4 " + str(Nodeid) + " " + str(Nodeip) + " " + str(Nodeport) # Message to meta-data server                    				  # String that contains the header and the command

s.sendall(message) # Send messahe to meta-data

confirm = s.recv(1024) # Confirmation from meta-data

s.close() # Close socket

if not os.path.exists("n" + str(Nodeid)): # If node directory does not exist

    os.makedirs("n" + str(Nodeid)) # Create Directory

else: # If Directory exists

	# Initialize Chunk id counter to the amount of files in the directory
	ChunkIdCount = len([name for name in os.listdir(os.getcwd() + "/n" + str(Nodeid))])

HOST = Nodeip                               # Symbolic name meaning all available interfaces

PORT = Nodeport                             # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.

s.bind((HOST, PORT))                                  # Bind socket to an address

s.listen(10)                                    	  # Stablishes the maximum of jobs that the socket can listen

while len(threads) != max_threads: # For each connection

	conn, addr = s.accept() #Starts accepting connections from the socket
	
	# Create new threads
	newthread = Handle_thread("Handle_thread", conn, addr)  # Create a thread that handles the connection

	newthread.start() # Start thread

	threads.append(newthread) # Store thread

for t in threads: # For each thread
	t.join() # Wait for each thread to finish

print "Exiting Main Thread"
s.close() # Close socket


