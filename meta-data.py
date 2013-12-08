###############################################################################
#
# Filename: meta-data.py
#
# Author: 
#		  
#		Jose R. Ortiz <2012>
#		Alex D. Santos Sosa <2013>
#		Ivan Jimenez
#
# Description:
#
#       The main purpose of this script is to provide meta data to the clients
#		When this script starts it listens for connections. If the connection
#		was stablished by a data-node it stores the meta-data of the datanode 
#		into the database. If the connections was stablihed by a client it checks
# 		the command that was issued and decides what to do. If the command was a
# 		list it return all the files that are stored in the DFS. Is the command 
#		was a write, it returns the available nodes and then stores the nodes the
#		client used to store the chunks. If the command was a read command it 
#		checks in the database what data nodes the client used to store that 
#		particular file and returns them to the client. Else the command is not
# 		recognized.
#
# Run:
#
#		- Open terminal
#		- Move to the containing folder
#		- run 'python list.py < meta-data server ip > < meta-data server port >
#		- i.e. python meta-data.py localhost 50003
#

# This is how to import a local library
from mds_db import * # Import local library
# This is how to import a local library
from sock import * # Import local library

#Libraries
import socket          # Library used for the socket functions in this program.
import threading       # Library used for the threads and its functions in the program.
import sys             # Library used for the inline parameters in this program.


# Handle Class Thread
class Handle_thread (threading.Thread):

	# Initialization of the thread
	def __init__(self, name, db, conn, addr):
		threading.Thread.__init__(self)
		self.name = name
		self.conn = conn
		self.addr = addr
		self.db = db
		print "Starting " + self.name

	# Define what the thread is to do
	def run(self):
		""" This thread will listen to the client messages from client.py and then print 
			the command the client wants to execute"""

		#data = conn.recv(640000000)  # Receive data from the socket.

		data = recv_msg(conn)

		data = str(data)

		if data[0] == str(0): 	# if header is 0

			print "list"	  	# command is list
			
			print
			
			info = db.MetaListFiles(db) # Custom List Function; See mds_db.py
			
			send_msg(conn, info) # Send succes to the socket.

			#conn.sendall(info) # Send succes to the socket.
			
			print

		elif data[0] == str(2):	# if header is 2
			
			print "read"		# command is read
			
			data = data.split(" ") # Split the message
			
			filepath = data[-1] # Get File path

			print filepath
			
			info = db.MetaFileRead(db, filepath) # Get data nodes where chunks are stored

			print info 

			send_msg(conn, info) # Send succes to the socket.
			
			#conn.sendall(info) # Send used nodes to the socket.

		elif data[0] == str(3):	# if header is 3
			
			print "write"		# command is write
			
			relation = [] # Stores the node to chunk relations
			
			data = data.split(" ") # Split the message
			
			filepath = data[-1] # Get filepath
			
			filesize = data[-2] # Get filesize
			
			db.InsertFile(filepath, filesize) # Insert file attributes into inode
			
			info = db.Book_Keeping(db) # Get available nodes

			send_msg(conn, info) # Send available nodes to socket
			
			#conn.sendall(info) # Send available nodes to socket

			data = recv_msg(conn)

			data = str(data)
			
			#data = conn.recv(640000000)  # Receive used nodes from the socket.
			
			data = data.split(",") # Split node to chunk relations
			
			for i in range (0, len(data)-1): # For each node to chunk relation
				
				temp = data[i].split(":") # Split the node from the chunk
				
				tup = (temp[0], temp[1]) # create a tuple with the node and the chunk
				
				relation.append(tup) # Store the tupple in the list
			
			db.MetaFileWrite(db, filepath, relation) # Custom Write Function; Store the relation
			
			conn.sendall("Success") # Send succes to the socket.
			
			print

		elif data[0] == str(4): # if header is 4
			
			print "creating node" # command is create a node
			
			info = data.split(" ") # Split the message
			
			db.AddDataNode("n" + info[1], info[2], info[3]) # Add data node to database
			
			conn.sendall("Node created") # Send succes to the socket. 
			
		else: # Command not recognized
			
			print "command not recognized"
			
			print

		conn.close()            # Close the connection.

# Create an object of type mds_db
db = mds_db() 

# Connect to the database
print "Connecting to database" 

db.Connect() 

max_threads = 20 # Maximum Threads allowed

threads = []*max_threads # Store threads

i = 0		 # Count Threads

HOST = ''                                             # Symbolic name meaning all available interfaces

PORT = int(sys.argv[1])                               # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.

s.bind((HOST, PORT))                                  # Bind socket to an address

s.listen(10)                                    	  # Establishes the maximum of jobs that the socket can listen

while len(threads) != max_threads: # For each connection

	conn, addr = s.accept() #Starts accepting connections from the socket
	# Create new threads
	newthread = Handle_thread("Handle_thread", db, conn, addr)  # Create a thread that hanldes the connection

	newthread.start()	# Start the thread

	threads.append(newthread)	# Store thread in a list

for t in threads: # For each thread

	t.join()	# Wait for each thread to join    

print "Exiting Main Thread"

s.close() # Close socket

db.Close() # Close DB connection