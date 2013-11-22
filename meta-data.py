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

# Producer Class Thread
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
			print

		elif data[0] == str(1):	# if header is 1
			print "copy"		# command is copy
			print

		elif data[0] == str(2):	# if header is 2
			print "read"		# command is read
			db.MetaFileRead(db, "/hola/cheo.txt") # Custom Read Function; See mds_db.py
			print

		elif data[0] == str(3):	# if header is 3
			print "write"		# command is write
			db.MetaFileWrite(db, "/hola/cheo.txt", [("n0", 1), ("n1", 1)]) # Custom Write Function; See mds_db.py
			print

		elif data[0] == str(4):
			print "creating node"
			db.AddDataNode("n" + str(NodeIdCount), "136.145.54.1" + str(NodeIdCount), 80)
			conn.sendall("n" + str(NodeIdCount)) # Send succes to the socket. 
			NodeIdCount += 1
			
		else:
			print "command not recognized"
			print

		if data[0] != str(4):
			conn.sendall("Success") # Send succes to the socket.

		conn.close()            # Close the connection.

# Create an object of type mds_db
db = mds_db() 

# Connect to the database
print "Connecting to database" 
db.Connect() 

max_threads = 5 # Maximum Threads allowed
threads = []*max_threads # Store threads
i = 0		 # Count Threads
NodeIdCount = 0

# Testing how to add a new node to the metadata server.
# Note that I used a node name, the address and the port.
# Address and port are necessary for connection.
'''
print "Testing node addition"
db.AddDataNode("n0", "136.145.54.10", 80) 
db.AddDataNode("n1", "136.145.54.11", 80) 
print 
print "Testing if node was inserted"
print "A tupple with node name and connection info must appear"
print db.CheckNode("n0")
print

print "Testing all Available data nodes"
for name, address, port in  db.GetDataNodes():
	print name, address, port

print 

print "Inserting two files to DB"
db.InsertFile("/hola/cheo.txt", 20)
db.InsertFile("/opt/blah.txt", 30)
print
'''
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