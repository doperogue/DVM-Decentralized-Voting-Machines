import socket
import websockets
import threading
# class for host

def host_IP():
    #determi the host name and ip
    # add a way to find ip and by trying 
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8",53))
        my_ip = s.getsockname()[0]
        s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        return my_ip

class peer():
    def __init__( self, maxpeers, serverport, myid=None, serverhost = None ):
        self.debug = 0

        self.maxpeers = int(maxpeers)
        self.serverport = int(serverport)

        # If not supplied, the host name/IP address will be determined
    # by attempting to connect to an Internet host like Google.
        if serverhost: self.serverhost = serverhost
        else: host_IP()

        # If not supplied, the peer id will be composed of the host address
        # and port number
        if myid: self.myid = myid
        else: self.myid = '%s:%d' % (self.serverhost, self.serverport)

        # list (dictionary/hash table) of known peers
        self.peers = {}  

        # used to stop the main loop
        self.shutdown = False  

        self.handlers = {}
        self.router = None
    # end constructor





        
    def findpeer():
        #retuens a list of peers
        return self.peers


    def makeserversocket( self, port, backlog=5 ):
        #socket.AF_Inet for ipv4 and sock_stream for tcp
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        s.bind( ( '', port ) )
        s.listen( backlog )
        return s
    def mainloop( self ):
        s = self.makeserversocket( self.serverport )
        s.settimeout(2)
        self.__debug( 'Server started: %s (%s:%d)'% ( self.myid, self.serverhost, self.serverport ) )

        while not self.shutdown:
            try:
                self.__debug( 'Listening for connections...' )
                clientsock, clientaddr = s.accept()
                clientsock.settimeout(None)

                t = threading.Thread( target = self.__handlepeer, args = [ clientsock ] )
                t.start()
            except KeyboardInterrupt:
                self.shutdown = True
                continue
            except:
                if self.debug:
                    traceback.print_exc()
                    continue
    # end while loop

        self.__debug( 'Main loop exiting' )
        s.close()
    # end mainloop method

    def __handlepeer( self, clientsock ):
        self.__debug( 'Connected ' + str(clientsock.getpeername()) )

        host, port = clientsock.getpeername()
        peerconn = BTPeerConnection( None, host, port, clientsock, debug=False )

        try:
            msgtype, msgdata = peerconn.recvdata()
            if msgtype: msgtype = msgtype.upper()
            if msgtype not in self.handlers:
                self.__debug( 'Not handled: %s: %s' % (msgtype, msgdata) )
            else:
                self.__debug( 'Handling peer msg: %s: %s' % (msgtype, msgdata) )
                self.handlers[ msgtype ]( peerconn, msgdata )
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()

        self.__debug( 'Disconnecting ' + str(clientsock.getpeername()) )
        peerconn.close()
    # end handlepeer method 

    def sendtopeer( self, peerid, msgtype, msgdata, waitreply=True ):
        if self.router:
            nextpid, host, port = self.router( peerid )
        if not self.router or not nextpid:
            self.__debug( 'Unable to route %s to %s' % (msgtype, peerid) )
            return None
        return self.connectandsend( host, port, msgtype, msgdata, pid=nextpid,waitreply=waitreply )

    # end sendtopeer method


# test 1
# test if i get ip

print(host_IP())


# propaget blocks
#create random overlay


#func to query chain 

# create seeder nodes 
#and do
# dns look up to get peer list


# form random outgoing and 