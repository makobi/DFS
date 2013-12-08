###############################################################################
#
# File name: meta-data.py
#
# Author: 
#		  
#		Jose R. Ortiz <2012>
#		Alex D. Santos Sosa  <2013>
#		Ivan L. Jimenez Ruiz <2013>
#
# Description:
#
#       The main purpose of this script is to provide meta data to the clients.
#		When this script starts, it listens for connections. If the connection
#		was established by a data-node, it stores the meta-data of the data-node 
#		into the database. If the connection was establihed by a client, it checks
# 		the command that was issued and decides what to do. If the command was a
# 		'list', it return all the files that are stored in the DFS. If the command 
#		was a write, it returns the available nodes and then stores the nodes the
#		client used for storing the chunks. If the command was a 'read', it 
#		checks in the database what data nodes the client used to store that 
#		particular file and returns them to the client. Else, the command is not
# 		recognized.
#
# How to Run:
#
#		- Open terminal
#		- Move to the containing folder
#		- Run 'python list.py < meta-data server ip > < meta-data server port >
#		- i.e. python meta-data.py localhost 50003
#

<<<<<<< HEAD
# This is how to import a local library
from mds_db import * # Import local library
# This is how to import a local library
from sock import * # Import local library
=======
from mds_db import * # Import local library.
>>>>>>> a4141d7798f410c2a6561ad1af0635fb73172bf2

#Libraries
import socket          # Library used for the socket functions in this program.
import threading       # Library used for the threads and thread functions in this program.
import sys             # Library used for the in-line parameters in this program.


# Handle Class Thread:
class Handle_thread (threading.Thread):

	# Initialization of the thread:
	def __init__(self, name, db, conn, addr):
		threading.Thread.__init__(self)
		self.name = name
		self.conn = conn
		self.addr = addr
		self.db = db
		print "Starting " + self.name

	# Define what the thread will do:
	def run(self):
		""" This thread will listen to the client messages from client.py and then print 
			the command the client wants to execute"""

		#data = conn.recv(640000000)  # Receive data from the socket.

		data = recv_msg(conn)

		data = str(data)

		if data[0] == str(0): 	# If header is 0:

			print "list"	  	# The command is "list".
			
			print
			
			info = db.MetaListFiles(db) # Custom List Function. (See: mds_db.py)
			
			send_msg(conn, info) # Send succes to the socket.

			#conn.sendall(info) # Send succes to the socket.
			
			print

		elif data[0] == str(2):	# If header is 2:
			
			print "read"		# The command is "read".
			
			data = data.split(" ") # Split the message.
			
			filepath = data[-1] # Get File path

			print filepath
			
			info = db.MetaFileRead(db, filepath) # Get data nodes where chunks are stored

			print info 

			send_msg(conn, info) # Send succes to the socket.
			
			#conn.sendall(info) # Send used nodes to the socket.

		elif data[0] == str(3):	# If header is 3:
			
			print "write"		# The command is "write".
			
			relation = [] # Stores the node-to-chunk relationships.
			
			data = data.split(" ") # Split the message.
			
			filepath = data[-1] # Get file path.
			
			filesize = data[-2] # Get file size.
			
			db.InsertFile(filepath, filesize) # Insert file attributes into i-node.
			
<<<<<<< HEAD
			info = db.Book_Keeping(db) # Get available nodes

			send_msg(conn, info) # Send available nodes to socket
			
			#conn.sendall(info) # Send available nodes to socket

			data = recv_msg(conn)

			data = str(data)
			
			#data = conn.recv(640000000)  # Receive used nodes from the socket.
			
			data = data.split(",") # Split node-to-chunk relationships.
			
			for i in range (0, len(data)-1): # For each node-to-chunk relationship:
				
				temp = data[i].split(":") # Split the node from the chunk.
				
				tup = (temp[0], temp[1]) # Create a tuple with the node and the chunk.
				
				relation.append(tup) # Store the tuple in the list.
			
			db.MetaFileWrite(db, filepath, relation) # Custom Write Function; Store the relationship.
			
			conn.sendall("Success") # Send succes to the socket.
			
			print

		elif data[0] == str(4): # If header is 4:
			
			print "Creating node" # The command is "create a node".
			
			info = data.split(" ") # Split the message at every space.
			
			db.AddDataNode("n" + info[1], info[2], info[3]) # Add data-node to database.
			
			conn.sendall("Node created") # Send succes to the socket. 
			
		else: # Command not recognized.
			
			print "Command not recognized"
			
			print

		conn.close()            # Close the connection.

# Create an object of type mds_db.
db = mds_db() 

# Connect to the database.
print "Connecting to database" 

db.Connect() 

max_threads = 20 # Maximum Threads allowed.

threads = []*max_threads # Store threads.

i = 0	# Count Threads.

HOST = ''                                             # Symbolic name, meaning all available interfaces.

PORT = int(sys.argv[1])                               # Arbitrary non-privileged port.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.

s.bind((HOST, PORT))                                  # Bind socket to an address.

s.listen(10)                                    	  # Establishes the maximum of jobs that the socket can listen for.

while len(threads) != max_threads: # For each connection:

	conn, addr = s.accept() #Starts accepting connections from the socket.
	# Create new threads
	newthread = Handle_thread("Handle_thread", db, conn, addr)  # Create a thread that handles the connection.

	newthread.start()	# Start the thread.

	threads.append(newthread)	# Store thread in a list.

for t in threads: # For each thread:

	t.join()	# Wait for each thread to finish.  

print "Exiting Main Thread"

s.close() # Close socket connection.

db.Close() # Close DB connection.
