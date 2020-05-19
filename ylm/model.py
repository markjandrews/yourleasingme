from ylm.config import config


class Model:
    def __init__(self, model_id, name):
        self.model_id = model_id
        self.name = name

    @classmethod
    def from_xml(cls, node):
        model_id = node.find('model_id').text
        name = node.find('name').text
        model = cls(model_id=model_id, name=name)
        return model

    def __repr__(self):
        return f'Model(model_id=\'{self.model_id}\', name=\'{self.name}\')'

