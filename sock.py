""" Library by Adam Rosenfield http://stackoverflow.com/users/9530/adam-rosenfield """

#Libraries
import socket              # Library used for the socket functions in this program.
import struct

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    print "send ", len(msg)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4) # Receive data
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0] # Unpack data
    print " receive", msglen
    # Read the message data
    return recvall(sock, msglen) # call function that uses len() if data is complete

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n: # if the size of the message is not equal to the total size
        packet = sock.recv(n - len(data)) # Keep receiving 
        if not packet:
            return None
        data += packet # accumulate message
    return data # return message