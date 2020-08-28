import socket
import websockets
import threading
import asyncio
import traceback
import json
from asyncio.exceptions import TimeoutError as ConnectionTimeoutError
# class for host
#to do change HELLO_MY_NAME_IS to IP address
#TODO make routing
#find peer adress by adding adress to site when acessed and share to peers 
HELLO_MY_NAME_IS ='server'
    #determi the host name and ip
    # add a way to find ip and by trying 
    #getes ip
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(("8.8.8.8",53))
    MY_IP = s.getsockname()[0]
    s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    s.close()




print(MY_IP)
# for referencing instance of task so when reference stops instance stops python garbage collec
CONNECTIONS= set()
# creata a super class fo all peers
class ConnectionHandeler:
    websocket = None
    hostname = None
    uri = None
    state = 'Disconnect'

    async def send(self,message):
        # func to send data 
        data = json.dumps(message)
        await self.websocket.send (data)

    async def recv(self):
        #func to receiver data
        try:
            message = await self.websocket.recv()  
            data = json.loads(message)
            return data
        except:
            traceback.print_exc() 

            #client sending
    async def login(self):
        try:
            self.websocket = await asyncio.wait_for(websockets.connect(self.uri),timeout=3)
        except ConnectionTimeoutError:
            print(f'ConnectionTimeout to:{self.uri}')
            return
        except ConnectionRefusedError:
            print(f'Connection refused to{self.uri}')
        except:
            return
        await self.send({'hostname':HELLO_MY_NAME_IS})

        challenge = await self.recv()



        if 'challenge' not in challenge or 'hostname' not in challenge:
            
            return
        if len(challenge['challenge'])>1024 or len(challenge['hostname']) >1024:

            return

        #TODO: password hashing Goes here
        self.hostname = challenge['hostname']
        password ={'password':'password'}

        await self.send(password)


        confirmation = await self.recv()
        confirmed = confirmation.get('connection')
        if confirmed =='authorised':

            self.state = 'Connected'
            print(f'connected to :{self.hostname}')
            return



    #client/peer connection
    

    async def welcome(self) -> bool:
        #serve/peer receiving
        #initial message is a declaration od a peer and seed important info to set up conn
        greeting = await self.recv()

        if 'hostname' not in greeting:
            return False
        #to prevent hackers dont accept insanley large values
        if len(greeting['hostname']) > 1024:
            return False


        self.hostname = greeting['hostname']
# challenge peer to confirm legitamacy
        challenge = {'challenge':'548thfweghwhruefewrewr','hostname':HELLO_MY_NAME_IS}

        await self.send(challenge)

        password = await self.recv()
        
#todo add actual password
        if 'password' not in password:
            return False
        if len(password['password']) > 1024:
            return False
        if password['password'] == 'password':
            await self.send({'connection':'authorised'})

            self.state ='Connected'
            print(f'new connection from :{self.hostname}')
            #creates listener which is all ways present and ehn con is closed if it is deinstanced task will dissaper
            asyncio.get_event_loop().create_task(self.listener())
            return True
        else:
            await self.send({'connection':'unauthorised'})
            return False



    async def listener(self):
        # listens for msg is instanciated and cn be deinstanciated
        try:
            async for message in self.websocket:
                print(message)
        except websockets.exceptions.ConnectionClosed:

            print(f"Connection closed drom {self.hostname}")
        except:
            traceback.print_exc()
        finally:
            await unregister(self)
 
    async def close(self): 
        try:
            
            await self.websocket.close()
            self.state='disconnected'
        except:
            traceback.print_exc()

class ServerHandeler(ConnectionHandeler):
    def __init__(self, websocket):
        self.websocket = websocket
class ClientHandeler(ConnectionHandeler):
    def __init__(self,uri):
        self.uri = uri

#TODO chnge to initial seed  peers
    
async def port_scan():
    #scans the local ips find any possible ip which connects to our port
    #only for testing
    # note port scaning is illegel make surr on private network 
    if not MY_IP[:3] == '192' and not MY_IP[:3]=='10.'and not MY_IP[:3] =='172':
        print('This is not a private network! Shutting DoWn')
        exit()
    ip_range =MY_IP.split('.')
    ip_range.pop()
    ip_range = '.'.join(ip_range)
    print(ip_range)

    #scan every ip in local range try connect
    i =101
    while i <255:
        i += 1 
        target_ip =f"{ip_range}.{i}"
        print(target_ip)
        uri =f"ws://{target_ip}:1111"
        
        connection = ClientHandeler(uri)
        await connection.login()
        if connection.state == 'Connected':
            CONNECTIONS.add(connection)
            asyncio.get_event_loop().create_task(connection.listener())

        await asyncio.sleep(0)


async def register_client(websocket,_):
    connection = ServerHandeler(websocket)
    done = False
    while True:
        if not done:
            if await connection.welcome():
        # the connec tion will persit in memory 
                CONNECTIONS.add(connection)
                done =True

        await asyncio.sleep(0)

async def unregister(connection):
    await connection.close()
    try:
        CONNECTIONS.remove(connection)
    except:
        traceback.print_exc()

async def status_update():
    while True:
        print(f'updating status...{len(CONNECTIONS)}')
        for connection in CONNECTIONS:
            if connection.state == "Connected":
                await connection.send({'hostname':HELLO_MY_NAME_IS,'connections':len(CONNECTIONS)})

        await asyncio.sleep(10)

if __name__ == "__main__":
    start_server = websockets.serve(register_client,MY_IP,1111)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().create_task(status_update())
    asyncio.get_event_loop().run_forever()







