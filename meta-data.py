###############################################################################
#
# Filename: meta-data.py
# Author: Jose R. Ortiz <Year>
#  		  Alex D. Santos Sosa <2013>
#		  Manuel
#		  Ivan Jimenez
#
# Description:
#       This is the meta data server.
#
#		<<<DESCRIPTION COMING SOON>>>
#

# This is how to import a local library
from mds_db import *

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

		global NodeIdCount

		print 'Connected by', addr #prints the connection

		data = conn.recv(1024)  # Receive data from the socket.

		if data[0] == str(0): 	# if header is 0
			print "list"	  	# command is list
			print
			db.MetaListFiles(db) # Custom List Function; See mds_db.py
			conn.sendall("Success") # Send succes to the socket.
			print

		elif data[0] == str(1):	# if header is 1
			print "copy"		# command is copy
			conn.sendall("Success") # Send succes to the socket.
			print

		elif data[0] == str(2):	# if header is 2
			print "read"		# command is read
			info = db.MetaFileRead(db, "/hola/cheo.txt")
			conn.sendall(info) # Send succes to the socket.

		elif data[0] == str(3):	# if header is 3
			print "write"		# command is write
			info = db.Book_Keeping(db)
			conn.sendall(info)
			data = conn.recv(1024)  # Receive data from the socket.
			data = data.split(",")
			relation = []
			for i in range (0, len(data)-1):
				temp = data[i].split(":")
				tup = (temp[0], temp[1])
				relation.append(tup)
			db.MetaFileWrite(db, "/hola/cheo.txt", relation) # Custom Write Function; See mds_db.py
			print data
			conn.sendall("Success") # Send succes to the socket.
			print

		elif data[0] == str(4):
			print "creating node"
			db.AddDataNode("n" + str(NodeIdCount), "136.145.54.1" + str(NodeIdCount), str(5000) + str(NodeIdCount))
			conn.sendall("n" + str(NodeIdCount) + " 136.145.54.1" + str(NodeIdCount) + " " + str(5000) + str(NodeIdCount)) # Send succes to the socket. 
			NodeIdCount += 1
			
		else:
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
NodeIdCount = 0

HOST = ''                                             # Symbolic name meaning all available interfaces
PORT = int(sys.argv[1])                               # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.bind((HOST, PORT))                                  # Bind socket to an address
s.listen(10)                                    	  # Establishes the maximum of jobs that the socket can listen

while len(threads) != max_threads:

	conn, addr = s.accept() #Starts accepting connections from the socket
	# Create new threads
	newthread = Handle_thread("Handle_thread", db, conn, addr)  # Initialize thread1 to Producer_thread class

	newthread.start()                           # Start thread1 Producer Thread

	threads.append(newthread)

for t in threads:
	t.join()                                        # Wait until the Thread1 finishes

print "Exiting Main Thread"
s.close() 