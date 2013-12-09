
###############################################################################
#
# File name: data-node.py
#
# Authors: 
#			Alex D. Santos Sosa  <2013>
#			Ivan L. Jimenez Ruiz <2013>
#
# Description:
#
#       The main purpose of this script is to create a data-node that stores
#		the chunks sent by the client. When the user runs this script, it sends
#		a message to the meta-data server indicating that it is alive and creates a
#		a directory in which the chunks are stored. When it receives a write command,
# 		it creates a file for the chunk and stores it. If it receives a copy command to
#		DFS, it reads the chunk and sends it to the client.
#
# How to Run:
#		
#		Pre-requisites - To run this script, the meta-data server must be up 
#						 and running. (See: meta-data.py)
#
#		- Open terminal
#		- Move to the containing folder
#		- Run 'python data-node.py < meta-data server ip > < meta-data server port > < data-node ID number > < data-node IP > < data-node port > < Path to Chunk Directory >
#		- i.e. python data-node.py localhost 30000 2 localhost 50002 ~/Assigment-4

# This is how to import a local library
from sock import * # Import local library

#Libraries
import socket          # Library used for the socket functions in this program.
import threading       # Library used for the threads and thread functions in this program.
import sys             # Library used for the in-line parameters in this program.


# Handle Class Thread:
class Handle_thread (threading.Thread):

	# Initialization of the thread:
	def __init__(self, name, conn, addr):
		threading.Thread.__init__(self)
		self.name = name
		self.conn = conn
		self.addr = addr
		print "Starting " + self.name

	# Define what the thread will to do:
	def run(self):
		""" This thread will listen to the client messages from client.py and then print 
			the command the client wants to execute"""

		global ChunkIdCount # ID for chunks.

		data = recv_msg(conn) # Receives a message from the client

		#data = conn.recv(640000000)  # Receives a message from the client

		info = data.split("//") # Split the message.

		if data[0] == str(0): # If command is 'copy to':

			file = open("n" + str(Nodeid)  + "/_bk" + str(ChunkIdCount) + '.dat', 'w') # Create file in node directory.

			file.write(str(info[2])) # Write the chunk into the file.

			file.close() # Close the file.

			send_msg(conn, str(ChunkIdCount)) # Send chunk id

			#conn.sendall(str(ChunkIdCount)) # Send chunk id

			ChunkIdCount += 1 # Increment chunk ID.

		elif data[0] == str(1): # If command is 'copy from':

			f = open("n" + str(Nodeid) + "/_bk" + str(info[1]) + '.dat', 'rb') # Open fie of chunk to read.

			Chunk = f.read() # Read the entire content of the file.

			f.close() # Close file.

			send_msg(conn, Chunk) # Send chunk

			#conn.sendall(Chunk) # Send chunk

		conn.close()            # Close the connection.

#Libraries
import socket              # Library used for the socket functions in this program.
import sys                 # Library used for the in-line parameters in this program.
import os				   # Library used for making directories

HOST = str(sys.argv[1]) # The remote host. In-line Parameter.

PORT = int(sys.argv[2]) # The same port the server uses. In-line Parameter.

Nodeid = int(sys.argv[3]) # Node ID.

Nodeip = str(sys.argv[4]) # Node IP address.

Nodeport = int(sys.argv[5]) # Node port.

NodeDirPath = str(sys.argv[6]) # Chunk dir

max_threads = 5 # Maximum Threads allowed.

ChunkIdCount = 0 # Initialize chunk ID counter.

threads = []*max_threads # Store threads.

message = "4 " + str(Nodeid) + " " + str(Nodeip) + " " + str(Nodeport) # Message to meta-data server.                   				  # String that contains the header and the command

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.

s.connect((HOST, PORT))                               # Connect to a remote socket at address. 

send_msg(s, message) # Send messahe to meta-data

#s.sendall(message) # Send messahe to meta-data

confirm = s.recv(1024) # Confirmation from meta-data server.

s.close() # Close socket connection.

if not os.path.exists(NodeDirPath + "/n" + str(Nodeid)): # If node directory does not exist

    try:
    	os.makedirs(NodeDirPath + "/n" + str(Nodeid)) # Create Directory

    except Exception, e:
    	raise e

else: # If Directory exists
	
	#os.makedirs("n" + str(Nodeid)) # Create Directory

	# Initialize chunk id counter to the amount of files in the directory.
	ChunkIdCount = len([name for name in os.listdir(NodeDirPath + "/n" + str(Nodeid))])

HOST = Nodeip                               # Symbolic name, meaning all available interfaces.

PORT = Nodeport                             # Arbitrary non-privileged port.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.

s.bind((HOST, PORT))                                  # Bind socket to an address.

s.listen(10)                                    	  # Establishes the maximum of jobs that the socket can listen for.

while len(threads) != max_threads: # For each connection:

	conn, addr = s.accept() # Start accepting connections from the socket.
	
	# Create new threads
	newthread = Handle_thread("Handle_thread", conn, addr)  # Create a thread that handles the connection.

	newthread.start() # Start thread.

	threads.append(newthread) # Store thread.

for t in threads: # For each thread:

	t.join() # Wait for each thread to finish.

print "Exiting Main Thread"
s.close() # Close socket connection.


