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
        self.__dict__ = json.loads(data)