from ylm.config import config


class Make:
    def __init__(self, make_id, name):
        self.make_id = make_id
        self.name = name

    @classmethod
    def from_xml(cls, node):
        make_id = node.find('make_id').text
        name = node.find('name').text
        make = cls(make_id=make_id, name=name)
        return make

    def __repr__(self):
        return f'Make(make_id=\'{self.make_id}\', name=\'{self.name}\')'

