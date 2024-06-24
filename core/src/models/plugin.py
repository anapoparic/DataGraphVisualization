class Plugin(object):
    def __init__(self, plugin, id: int, description: str = ''):
        self.plugin = plugin
        self.id = id
        self.description = description
