from ylm.config import config


class Quote:
    def __init__(self, **kwargs):

        for k, v in kwargs.items():
            if not v or not v.strip():
                # print(f'*** WARNING *** No value for "{k}"')
                continue

            v = v.strip()
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
