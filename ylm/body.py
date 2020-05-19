from ylm.config import config


class Body:
    def __init__(self, body_type_id, body_type):
        self.body_type_id = body_type_id
        self.body_type = body_type

    @classmethod
    def from_xml(cls, node):
        body_type_id = node.find('body_type_id').text
        body_type = node.find('body_type').text
        body = cls(body_type_id=body_type_id, body_type=body_type)
        return body

    def __repr__(self):
        return f'Body(body_type_id=\'{self.body_type_id}\', body_type=\'{self.body_type}\')'

