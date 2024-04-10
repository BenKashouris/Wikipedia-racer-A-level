import socket
import json
from tkinter import EXCEPTION
from typing import Tuple

from select import select

class SocketController:
    """Socket Controller for client"""
    def __init__(self, IP: str, port: int):
        self._IP, self._port = IP, port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #try to connect to server
        self.socket.connect((IP, port))

    def send(self, func_name: str, data: str):
        """Send to the client"""
        data = json.dumps(data)
        ##print("{0}-{1}".format(func_name, data))
        self.socket.send(bytes("{0}-{1}".format(func_name, data), "UTF-8"))

    def receive(self) -> Tuple[str, dict]:
        """Recieve a response from the server of arbitrary length"""
        message = self.socket.recv(1024).decode("UTF-8")
        while message.count("{") != message.count("}"): # Make sure that the message is fully complete
            message += self.socket.recv(1024).decode("UTF-8")
        func_name, data = message.split("-")
        return (func_name, json.loads(data))

    def is_readable(self) -> bool:
        """See if this socket has a message waiting"""
        return bool(select([self.socket], [], [], 0)[0])
