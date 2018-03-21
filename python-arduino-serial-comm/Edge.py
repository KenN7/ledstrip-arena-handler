import json


class Edge(object):
    """ 
    """

    def __init__(self, data):
        """ 
        """
        self.index = 0
        self.color = ""
        self.block = []
        self.led = []
        self.__dict__ = json.loads(data)