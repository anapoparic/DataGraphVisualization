class Config(object):
    def __init__(self, name: str, key: str, data_type: type):
        self.name = name
        self.key = key
        self.data_type = data_type
