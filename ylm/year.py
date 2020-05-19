from ylm.config import config


class ModelYear:
    def __init__(self, model_year):
        self.model_year = model_year

    @classmethod
    def from_xml(cls, node):
        model_year = node.find('model_year').text
        year = cls(model_year=model_year)
        return year

    def __repr__(self):
        return f'ModelYear(model_year=\'{self.model_year}\')'

