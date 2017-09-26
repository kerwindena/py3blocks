class BlockProperties(dict):
    property_names = {
        'align': 'align',
        'color': 'color',
        'full_text': 'full_text',
        'instance': 'instance',
        'min_width': 'min_width',
        'seperator': 'seperator',
        'seperator_block_width': 'seperator_block_width',
        'short_text': 'short_text',
        'urgent': 'urgent',

        '_command': 'command',
        '_interval': 'interval',
        '_label': 'label',
        '_signal': 'signal',
        '_timeout': 'timeout',
    }

    def __init__(self, name):
        for prop in self.property_names:
            self[prop] = None
        self['name'] = name

    def read(self, config):
        changed = False
        for k, v in self.property_names.items():
            value = config.get(self['name'], v, fallback=None)
            if value != self[k]:
                changed = True
                self[k] = value
        return changed
