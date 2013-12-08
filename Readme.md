# Simple Distributed File System

## Authors:
#### Alex D. Santos Sosa ( @Makobi )    Computer Science Department, University of Puerto Rico, Rio Piedras
#### Ivan L. Jimenez Ruiz ( @NacroKill ) Computer Science Department, University of Puerto Rico, Rio Piedras

## Libraries:

+ Local:
    - mds_db.py ( Database functions )
    - sock.py ( Socket data transfer functions )
+ Global:
    - Threading ( Multi-threading )
    - MySQLdb ( SQL Database )
    - Struct ( Data Transfer )
    - Socket ( Create Sockets )
    - Sys ( Command line arguments )
    - Os ( File handling)

## DFS File Composition:

- meta-data.py ( Meta Data Server )
- data-node.py ( Data Server Node )
- list.py ( List client )
- cp.py ( Copy client )
 
## meta-data.py ( Meta Data Server ):

  * Description:
      - The main purpose of this script is to provide meta data to the clients.
        When this script starts, it listens for connections. If the connection
        was established by a data-node, it stores the meta-data of the data-node 
        into the database. If the connection was establihed by a client, it checks
        the command that was issued and decides what to do. If the command was a
        'list', it return all the files that are stored in the DFS. If the command 
        was a write, it returns the available nodes and then stores the nodes the
        client used for storing the chunks. If the command was a 'read', it 
        checks in the database what data nodes the client used to store that 
        particular file and returns them to the client. Else, the command is not
        recognized.
  
  * Algorithm:
      1. Connects to the database
      2. Listens for connections
      3. When connection is made create a handle thread
      4. Thread checks for the command issued
      5. Queries the database
      6. Responds with informations requested
      7. Depending on the command waits for further comunication or terminates the connection
  
  * How to Run:
      1. Open terminal
      2. Move to the containing folder
      3. Run 'python list.py < meta-data server ip > < meta-data server port >
      4. i.e. python meta-data.py localhost 50003

## data-node.py ( Data Server Node ):

  * Description:
      - The main purpose of this script is to create a data-node that stores
        the chunks sent by the client. When the user runs this script, it sends
        a message to the meta-data server indicating that it is alive and creates a
        a directory in which the chunks are stored. When it receives a write command,
        it creates a file for the chunk and stores it. If it receives a copy command to
        DFS, it reads the chunk and sends it to the client.

  * Algorithm
      1. Sends message to meta data server with its attributes i.e id, port, ip
      2. Creates directory if not allready created
      3. If directory was allready created it checks for the amount of files in the directory to set the chunk id counter
      4. Listens for connections
      5. When a connection is received it creates a handle thread the handles the connection
      6. The thread checks if it's a read or a write
      7. If it is a write it stores the chunk in a file and sends the chunk id to the client
      8. If it is a read it reads the chunk from the file and send it to the client
  
  * How to Run:
      - Pre-requisites:
          * To run this script, the meta-data server must be up 
						and running. (See: meta-data.py)
      
      - Run: 
        1. Open terminal
        2. Move to the containing folder
        3. Run 'python data-node.py < meta-data server ip > < meta-data server port > < data-node ID number > < data-node           IP > < data-node port > < Path to Chunk Directory >
        4. i.e. python data-node.py localhost 30000 2 localhost 50002 ~/Assigment-4

## list.py ( List Client ):

  * Description:
      - The main purpose of this script is to handle the list command
        issued by the user. When the user runs this script, the script 
        connects to the meta-data server using the command-line arguments
        provided by the user. After the connection is established, the 
        the meta-data server responds with the data the script requested
        i.e. all the files in the DFS. After the data is received, the
        the scripts parses the data to separate the information of each file
        and prints it.
    
  * Algorithm:
      1. Send a message to the meta data server requesting a list of all the files in the FS 
      2. Receives and splits the information returned by the meta data server
      3. Prints all the files in the FS

    * How to Run:
      -	Pre-requisites: 
          * To run this script the meta-data server must be up 
            and running. (See: meta-data.py)
      - Run:
          1. Open terminal
          2. Move to the containing folder
          3. Run 'python list.py < meta-data server ip > < meta-data server port >
          4. i.e. python list.py localhost 50003
          
## cp.py ( Copy Client ):

  * Description:
      - The main purpose of this script is to handle the copy command
        issued by the user. When the user runs this script, the script 
        connects to the meta-data server using the command-line arguments
        provided by the user. After the connection is established the 
        the meta-data server responds with the data the script requested,
        i.e. all the available nodes. After the data is received, the
        the scripts parse the data to separate the information of each node,
        connects to each of them and sends them the chunks of the file. 
        After the chunks are stored the client sends the nodes it used to
        store the chunks to the meta-data server.
    
  * Algorithm:
      1. If it is a copy to the DFS
      2. It contacts the meta data server to check what data nodes are available
      3. Then it decides which nodes it is going to use
      4. It splits the file using a chunk size to available nodes ratio
      5. Sends the chunks to a respective data node
      6. Receives the chunk ids
      7. Sends the meta data of the chunks to the meta data server
      8. If it is a copy to from the DFS
      9. It contacts the meta data server to obtain in which data nodes are the chunks stored
      10. Connects with each of the nodes requesting the chunks
      11. Concatenates the chunks and creates a file using the path the user input

    * How to Run:
      -	Pre-requisites: 
          * To run this script, the meta-data and the data node 
            servers must be up and running. (See: meta-data.py and data-node.py)
      - Run:
          1. Open terminal
          2. Move to the containing folder
          3. Run 'python cp.py < Command > < Path to file in computer > < meta-data server ip > < meta-data server port               >:< Path to file in DFS >
          4. i.e. python cp.py -t /Users/Makobi/Documents/hola.txt localhost 30001:Desktop/Test.txt
          5. i.e. python cp.py -f /Users/Makobi/hola.txt localhost 30001:Desktop/Test.txt
