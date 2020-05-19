from ylm.config import config


class Variant:
    def __init__(self, *, variant_id, description, **kwargs):
        self.variant_id = variant_id
        self.description = description

        for k, v in kwargs.items():
            setattr(self, k, v)

        str_params = ', '.join((f'{k}=\'{v}\'' for k, v in self.__dict__.items()))
        self.repr_str = f'Variant({str_params})'

    @classmethod
    def from_xml(cls, node):
        params = {}
        for item in node:
            params[item.tag] = item.text

        variant = cls(**params)
        return variant

    def __repr__(self):
        return self.repr_str
