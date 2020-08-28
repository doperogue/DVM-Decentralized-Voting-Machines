import socket
import websockets
import threading
import asyncio
import traceback
import json
from asyncio.exceptions import TimeoutError as ConnectionTimeoutError
# class for host

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
CONNECTIN = set()
# creata a super class fo all peers
class ConnectionHandeler:
    websocket = None
    hostname = None
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

    

    async def welcome(self) -> bool:
        #initial message is a declaration od a peer and seed important info to set up conn
        greeting = await self.recv()

        if 'hostname' not in greeting:
            return False
        #to prevent hackers dont accept insanley large values
        if len(greeting['hostname']) > 1024;
            return False


        self.hostname = greeting['hostname']
# challenge peer to confirm legitamacy
        challenge = {'challenge':'548thfweghwhruefewrewr'}

        await self.send(challenge)

        password = await self.recv()

#todo add actual password
        if 'password' not in password:
            return False
        if len(password['password']) > 1024:
            return False
        if password['password'] == 'password':
            self.state ='Connected'
            #creates listener which is all ways present and ehn con is closed if it is deinstanced task will dissaper
            asyncio.get_event_loop().create_task(self.listener())
            return True

        return False



    async def listener(self):
        # listens for msg is instanciated and cn be deinstanciated
        try:
            async for message in self.websocket:
                print(message)
        except websockets.exceptions.ConnectionClosed:
            print(f"Connection closed drom {self.hostname}")
 
    async def close(self):
        try:
            self.websocket.close()
        except:
            traceback.print_exc()

class ServerHandeler(ConnectionHandelern):
    def __init__(self, websocket):
        self.websocket = websocket
    

    
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
        try:
            connection = await asyncio.wait_for(websockets.connect(uri),timeout=5) 
            await connection.send('hello')
            async for message in connection:
                print(message)
        except ConnectionRefusedError:
            print("server connection refused")
            pass
        except ConnectionError:
            pass
        except ConnectionTimeoutError:
            print(f"timeout:{target_ip}")
            pass
        except TimeoutError:
            pass
        except websockets.exceptions.ConnectionClosed:
            pass
        except:
            traceback.print_exc()



async def register_client(websocket,_):
    async for message in websocket:
        print(message)
        await websocket.send("hello yourself")


if __name__ == "__main__":
    start_server = websockets.serve(register_client,MY_IP,1111)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()







