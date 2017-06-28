import json

from .BlockProvider import BlockProvider


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            if isinstance(o, BlockProvider):
                if not o.block['full_text']:
                    return None
                return {k: v for k, v in o.block.items()
                        if not k.startswith('_') and v is not None and len(str(v)) > 0}
            return [x for x in o.get_blocks().values() if self.default(x) is not None]
        except AttributeError:
            pass
        return json.JSONEncoder.default(self, o)
