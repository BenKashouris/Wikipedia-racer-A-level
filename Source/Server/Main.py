import SocketController
import Decoder
import ApplicationFunction

import socket

server = SocketController.SocketController(socket.gethostbyname(socket.gethostname()), 6677, 1024)

function_switch = {"sign_up": ApplicationFunction.sign_up,
                    "log_in": ApplicationFunction.log_in,
                    "get_leaderboard": ApplicationFunction.get_leaderboard,
                    "get_titles": ApplicationFunction.get_titles,
                    "packet_error": ApplicationFunction.error_packet,
                    "queue": ApplicationFunction.queue,
                    "get_chain": ApplicationFunction.get_chain,
                    "make_move": ApplicationFunction.make_move}

while True:
    server.accept_clients()
    requests = server.get_requests()
    requests = list(map(Decoder.decode, requests))
    for request in requests:
        function_switch[request.func_name](request.client, **request.parameters)  # Run the function with the data inputed as kwargs

