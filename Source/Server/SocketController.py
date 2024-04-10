"""Module that defines a SocketController capable of multiple simtanelous connections"""
import socket
from select import select
from datetime import datetime
from typing import List

class ClientSocket:
    """Object that represents a client"""
    def __init__(self, socket, IP: str, port: int, bufsize: int):
        self._socket, self._IP, self._port, self._bufsize = socket, IP, port, bufsize
        self._conn_time = datetime.now()

    def is_readable(self) -> bool:
        """Check if this Client has a message avalibale, this function is none blocking"""
        return bool(select([self._socket], [], [], 0)[0])  # if the list is empty we know this client is not readable

    def get_message(self) -> str:
        """get the client message, this function is blocking"""
        return self._socket.recv(self._bufsize).decode("UTF-8")

    def send_message(self, msg: str) -> None:
        """send a message to a client, this function is blocking"""
        #print('{0}: Server said "{1}" to {2}'.format(datetime.now(), msg, self))
        self._socket.send(bytes(msg, "utf-8"))

    def close(self):
        """close a client"""
        self._socket.close()

    def __repr__(self) -> str:
        return "({0}, {1})".format(self._IP, self._port)

    def get_session_id(self) -> int:
        """Get a session unique ID
        returns a string"""
        return hash(self._IP + str(self._port) + str(self._conn_time))

class Request:
    """Data Class that hold client of a request, the message of a request, and the datetime"""
    def __init__(self, client: ClientSocket, msg: str, datetime: datetime):
        self.client, self.msg, self.datetime = client, msg, datetime

    def __repr__(self):
        return '{0}: {1} said "{2}"'.format(self.datetime, self.client, self.msg)

class SocketController:
    """Object that can be used in order to accept connections and recieve messages from multiple clients
        Paramters:
            IP: a string with the IP of the host machine
            Port: a integer that the server should use
            bufsize: maximum data to read at one time"""

    def __init__(self, IP: str, port: int, bufsize: int):
        self._IP, self._port, self._bufsize = IP, port, bufsize
        self._clients: List[ClientSocket] = []

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._IP, self._port))
        self._socket.listen()
        self._socket.setblocking(False)

    def accept_clients(self) -> None:
        """Accept a new clients"""
        if select([self._socket], [], [], 0)[0] == []: return  # If no clients to connect to leave
        socket, (IP, port) = self._socket.accept()
        self._clients.append(ClientSocket(socket, IP, port, self._bufsize))
        print("{0}: {1} connected on client port {2}".format(datetime.now(), IP, port))

    def close_client(self, client: ClientSocket) -> None:
        """Close a client"""
        print("{0}: Closing {1}".format(datetime.now(), client))
        client.close()
        self._clients.remove(client)
        
    def get_requests(self) -> List[Request]:
        """Returns a list of requests objects"""
        requests: List[Request] = []
        for client in self._clients:
            if not client.is_readable(): continue
            try:
                request_msg: str = client.get_message()
            except WindowsError as e:  # If the client has had a unexpected error then close it
                print("{0}: {1} has experinced a error".format(datetime.now(), client))
                self.close_client(client)
                continue
            if request_msg == "":  # If the client closes the socket then close it on the server side
                self.close_client(client)
            else:  # Else make request object
                request = Request(client, request_msg, datetime.now())
                requests.append(request)
               #print(request)
        return requests
