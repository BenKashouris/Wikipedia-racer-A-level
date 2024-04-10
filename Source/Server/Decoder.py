"""Module defining a function to turn a request to a decoded request"""
import json
from SocketController import *
import re
from typing import Dict



_GENERAL_REQUEST_REGEX = re.compile(r"""([a-z]|_)+-{([a-z]|{|}|[|]|:|(|)|"|'| |,|.)*}""")
function_parameters = {"sign_up": [("username", str), ("password", str)],  # Given the function name return the name of the parameter and what data type it should be
                        "log_in": [("username", str), ("password", str)],
                        "get_leaderboard": [],
                        "make_move": [("pageID", int)],
                        "queue": [],
                        "get_titles": [("pageIDs", list)],
                        "get_chain": [("start_pageID", int), ("end_pageID", int)]}

class DecodedRequest():
    """A decoded request is a request with a the func_name and paramters / data split as well as a decoder client"""
    def __init__(self, client: ClientSocket, func_name: str, parameters: Dict, datetime: datetime):
        self.client, self.func_name, self.parameters, self.datetime = EncoderClient(client), func_name, parameters, datetime

    def __repr__(self):
        return '{0}: {1} said "{2}"'.format(self.datetime, self.client, self.msg)

def create_error_request(client, msg: str, datetime) -> DecodedRequest:
    return DecodedRequest(client, "packet_error", {"message": msg}, datetime)

def decode(request: Request) -> DecodedRequest:
    """Decode a request and return a decoded request"""
    if not re.fullmatch(_GENERAL_REQUEST_REGEX, request.msg): ## Check that the request follows func name dash data standard
        return create_error_request(request.client, """Does not follow "function_name"-"data" standard""", request.datetime)
    func_name, data = request.msg.split("-")  # Split the function and data
    try:
        data = json.loads(data)  # Attempt to load the json
    except ValueError:
        return create_error_request(request.client, "Data is not json", request.datetime)
    if not (type(data) == dict): # check data is a dictionary
        return create_error_request(request.client, "Data is not a dictionary", request.datetime)
    parameters_needed = function_parameters.get(func_name)  # Get the paramters needed
    if parameters_needed == None:  # If there arent any paramters for this function the function doesnt exist
        return create_error_request(request.client, "Function asked for does not exist", request.datetime)
    if len(data) != len(parameters_needed):  # Check the amount of paramters needed is the amount this request has
        return create_error_request(request.client, "The amount parameters given was not expected", request.datetime)
    for parameter_name, parameter_type in parameters_needed:
        # Check where if the parameter needed is in the data
        if data.get(parameter_name) == None: return create_error_request(request.client, "A parameter needed was not given", request.datetime)
        if type(data.get(parameter_name)) != parameter_type: # Check if parameter was correct type
            return create_error_request(request.client, "Parameter " + parameter_name + " was not correct type", request.datetime)
    return DecodedRequest(request.client, func_name, data, request.datetime)

class EncoderClient:
    """Client with a better send method"""
    def __init__(self, client: ClientSocket):
        self.client: ClientSocket = client

    def send(self, func_name: str, data: dict) -> None:
        """Send a message to the client
        parameters: func_name, the protocol function/service used
                    data, the protocol data"""
        data = json.dumps(data)  # Make the json string
        self.client.send_message("{0}-{1}".format(func_name, data))

    def get_session_id(self):
        return self.client.get_session_id()

    def __repr__(self):
        return str(self.client)
