
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
#		<<< DESCRIPTION COMING SOON >>>
#

#Libraries
import socket          # Library used for the socket functions in this program.
import threading       # Library used for the threads and its functions in the program.
import shutil # Library used for the transfer of files to specific directories.
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

		global ChunkIdCount

		print 'Connected by', addr #prints the connection

		data = conn.recv(640000000)  # Receive data from the socket.

		info = data.split("//")

		if data[0] == str(0):

			file = open("n" + str(Nodeid)  + "/_bk" + str(ChunkIdCount) + '.dat', 'w')

			file.write(str(info[2]))

			file.close()

			conn.sendall(str(ChunkIdCount)) # Send succes to the socket.

			ChunkIdCount += 1

		elif data[0] == str(1):

			f = open("n" + str(Nodeid) + "/_bk" + str(info[1]) + '.dat', 'rb')

			Chunk = f.read() # read the entire content of the file

			f.close()

			conn.sendall(Chunk) # Send succes to the socket.

		conn.close()            # Close the connection.

#Libraries
import socket              # Library used for the socket functions in this program.
import sys                 # Library used for the inline parameters in this program.
from time import sleep     # Library used for the sleep function in this program.
import os				   # Library used for making directories

HOST = str(sys.argv[1]) # The remote host. Inline Parameter.
PORT = int(sys.argv[2]) # The same port as used by the server. Inline Parameter.
Nodeid = int(sys.argv[3]) 
Nodeip = "localhost"
Nodeport = int(sys.argv[4])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.connect((HOST, PORT))                               # Connect to a remote socket at address. 

max_threads = 5 # Maximum Threads allowed
ChunkIdCount = 0
threads = []*max_threads # Store threads
message = "4 " + str(Nodeid) + " " + str(Nodeip) + " " + str(Nodeport)                     				  # String that contains the header and the command
s.sendall(message)                                     # Send data to the socket.
confirm = s.recv(1024)  
print confirm
s.close()

if not os.path.exists("n" + str(Nodeid)):
    os.makedirs("n" + str(Nodeid))
else:
	ChunkIdCount = len([name for name in os.listdir(os.getcwd() + "/n" + str(Nodeid))])

HOST = Nodeip                                             # Symbolic name meaning all available interfaces
PORT = Nodeport                             # Arbitrary non-privileged port
print HOST
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new socket.
s.bind((HOST, PORT))                                  # Bind socket to an address
s.listen(10)                                    	  # Establishes the maximum of jobs that the socket can listen

while len(threads) != max_threads:

	conn, addr = s.accept() #Starts accepting connections from the socket
	# Create new threads
	newthread = Handle_thread("Handle_thread", conn, addr)  # Initialize thread1 to Producer_thread class

	newthread.start()                           # Start thread1 Producer Thread

	threads.append(newthread)

for t in threads:
	t.join()                                        # Wait until the Thread1 finishes

print "Exiting Main Thread"
s.close()


