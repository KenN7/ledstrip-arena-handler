import json


class Led(object):
    """ 
    """

    def __init__(self, data):
        """ 
        """
        self.index = 0
        self.color = ""
        self.__dict__ = json.loads(data)
