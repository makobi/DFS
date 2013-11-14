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
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name
		print "Starting " + self.name

	# Define what the thread is to do
	def run(self):
		""" This thread will listen to the client messages from client.py and then print 
			the command the client wants to execute"""

		while True:

			conn, addr = s.accept() #Starts accepting connections from the socket

			print 'Connected by', addr #prints the connection

			data = conn.recv(1024)  # Receive data from the socket.

			if data[0] == str(0): 	# if header is 0
				print "list"	  	# command is list

			elif data[0] == str(1):	# if header is 1
				print "copy"		# command is copy

			elif data[0] == str(2):	# if header is 2
				print "read"		# command is read

			elif data[0] == str(3):	# if header is 3
				print "write"		# command is write

			else:
				print "command not recognized"

			if not data: break

			conn.sendall("Success") # Send succes to the socket.

			conn.close()            # Close the connection.

# Create an object of type mds_db
db = mds_db() 

# Connect to the database
print "Connecting to database" 
db.Connect() 

# Testing how to add a new node to the metadata server.
# Note that I used a node name, the address and the port.
# Address and port are necessary for connection.

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

HOST = ''                                             # Symbolic name meaning all available interfaces
PORT = int(sys.argv[1])                               # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.bind((HOST, PORT))                                  # Bind socket to an address
s.listen(10)                                    	  # Stablishes the maximum of jobs that the socket can listen

# Create new threads
thread1 = Handle_thread("Handle_thread")          	  # Initialize thread1 to Producer_thread class

# Start new Threads
thread1.start()                                       # Start thread1 Producer Thread

thread1.join()                                        # Wait until the Thread1 finishes

# Below is an atempt to use multi-threading
"""while True:
	conn, addr = s.accept() #Starts accepting connections from the socket
	# Create new threads
	threads[i] = Producer_thread("Producer_thread")          # Initialize thread1 to Producer_thread class
	#thread2 = Consumer_thread("Consumer_thread")          # Initialize thread2 to Consumer_thread class

	# Start new Threads
	threads[i].start(conn, addr)                                       # Start thread1 Producer Thread
	#thread2.start()                                       # Start thread2 Consumer Thread
	threads[i].join()                                        # Wait until the Thread1 finishes
	#thread2.join()                                        # Wait until the Thread2 finishes
	i = i+1"""

print "Exiting Main Thread"
s.close() 