import socket
import threading

class peer():
	"""docstring for peer"""
	# modify max perrs according to condition
	def __init__(self, maxpeers,peerport,myid=None,peerhost=None):
		self.maxpeers = maxpeers
		self.peerport = serverport
		# if not suppiled find hostname /IP by trying to connect internet host lick google 
		if serverhost:self.serverhost = serverhost
		else: self.__initserverhost() 

		#list of known peers 
		self.peers = {}
		#use to shut down the peer thread
		self.shutdown = False
		self.router = None
		self.handeler = None




	def __initserverhost()
	#determin the host name and ip
		print("see")
	def findpeer()
		#retuens a lis of peers
		return self.peers

	
	def makeserversocket( self, port, backlog=5 ):
		s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		s.bind( ( '', port ) )
		s.listen( backlog )
		return s
	

# propaget blocks
#create random overlay


#func to query chain 

# create seeder nodes 
#and do
# dns look up to get peer list


# form random outgoing and 