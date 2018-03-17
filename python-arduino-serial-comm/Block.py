import json


class Block(object):
    """ 
    """

    def __init__(self, data):
        """ 
        """
        self.index = 0
        self.color = ""
        self.led = []
        self.__dict__ = json.loads(data)
