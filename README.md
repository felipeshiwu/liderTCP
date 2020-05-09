# liderTCP

Work implemented in Python using threads to elect a leader among several connected machines, each sends a heartbeat every period of time and a new leader is chosen whenever the current leader is disconnected. The leader is chosen based on the lowest ID.

System requirements

Firstly, it is necessary to create the 'entry' file in the same directory as the code and containing the necessary information so that the system can make the necessary connections. As the file is read line by line, the information must be in the following structure:

1st line, contains the number of peers.

2nd line onwards contains the ID followed by the IP of the machines, always one machine per line

Example: 

> 4
>
> 0 192.168.0.6
>
> 1 192.168.0.7
>
> 2 192.168.0.8
>
> 3 192.168.0.9

*It is important to remember that the relationship between IDs and IPs must be respected throughout the process and the same 'input' file must be used for all machines.

# System initialization

Once this is done, we can run the program, for that, just run the python program with the first argument being its own ID and the second argument the port that the connection will be made. Example: python peer.py 0 5621
Then, the program takes the information taken from the 'entry' file and stored in a list called IPs, this list offers the information that will be used to send messages and identify the machines' IPs based on the IDs, even your own ID is obtained thus. When reading, the heartbeats dictionary, which has IDs as its key, starts with zero and we add the IDs to the list of online machines. A thread is also created so that the peer can listen for messages coming along with a thread to check TIMEOUTS, but it will only start when everyone is connected. Here he remains waiting until all the other machines are connected.

So far, some important decisions have been made, one of which is that the heartbeats dictionary will store the time he received the message, already thinking about later using TIMEOUT to find the machines that have disconnected. Along with this, the way to know that all machines are connected, is to verify that all heartbeats are different from 0 (zero). A list of machines was also created which is initially filled in with all the IDs in the 'entry' file, it may be a little hasty to put all machines online before they are actually connected, but as it is necessary that all machines are connected to starting the whole process of electing the leader and actually working does not affect the functioning in any way.
As for the messages, we decided that it would simply be your own ID, as it is easy to handle and we can easily find your IP by the IP list, we had this inspiration from heartbeats, as it is suggestive to understand that it is just a message to know that you are alive and naturally knowing who is alive.

# System execution

The sending of messages is based on the IDs that are in the list of online machines and we define frequency as 2s. After all machines are connected, the heartbeat dictionary is completed with the time it received the messages and the first election is made. The result of the election is the lowest ID in the list of online machines. The list of online machines is changed when TIMEOUT verifies that the time since a given machine sent a message to it has exceeded a time that we defined as 5s, consequently, the ID of that machine is removed from the list and if the ID was of the leader, it is made a new election. At that moment, urgent messages come into action, we use the MSG_OOB flag, they warn others that a leader update is needed.

# The flow is basically as follows:

1. The peer sends its ID to all machines in the list of online machines

2. When the heartbeat is received, we record its arrival time in the heartbeats dictionary for the sender's ID.

3. In parallel, every 2 seconds the peers send their heartbeat.

4. Also in parallel, TIMEOUT always arrives if the time since the last connection has exceeded 5s. If so, check if you are the leader, if you have lost connection with the leader, we send an urgent message and elect a new leader, if not the leader, we just remove it from the list of online machines.

