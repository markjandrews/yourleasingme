import requests

import lxml.etree

# top_manufacturers = ['100035', '100053', '100057', '100023', '100039', '100059', '100021', '100020', '100028', '100017']
from ylm.body import Body
from ylm.config import config
from ylm.make import Make
from ylm.model import Model
from ylm.quote import Quote
from ylm.variant import Variant
from ylm.year import ModelYear

base_uri = 'https://www.smartleasing.com.au/'


def get_makes():
    root = web_request('POST', 'make', None)
    makes = {}
    for node in root:
        child = Make.from_xml(node)
        makes[child.make_id] = child

    return makes


def get_models(make):
    root = web_request('POST', 'process', {'make_id': make.make_id})

    models = {}
    for node in root:
        child = Model.from_xml(node)
        models[child.model_id] = child

    return models


def get_years(model):
    root = web_request('POST', 'year', {'model_id': model.model_id})

    years = set()
    for node in root:
        child = ModelYear.from_xml(node)
        years.add(child.model_year)

    return sorted(list(years), reverse=True)


def get_bodies(model, year):
    bodies = {}
    root = web_request('POST', 'body', {'year_id': year, 'model_id': model.model_id})

    if root is None:
        return None

    for node in root:
        child = Body.from_xml(node)
        bodies[child.body_type_id] = child

    return bodies


sess = requests.Session()


def web_request(method, func, data):
    assert method in ['GET', 'POST']

    uri = '/'.join(x.rstrip('/') for x in [base_uri, func])
    rsp = sess.request(method, uri, data=data)
    rsp.raise_for_status()

    # print(rsp.content.decode())
    parser = lxml.etree.XMLParser(recover=True)
    root = lxml.etree.fromstring(rsp.content, parser)

    if root is not None:
        if len(root) == 0 and root.tag == 'error':
            print(f'*** WARNING *** - {uri} {data} ({root.text})')
            return None
    else:
        root = rsp.json()

    return root


def get_variants(body, year, model):
    variants = {}
    root = web_request('POST', 'variant',
                       {'body_type_id': body.body_type_id, 'year_id': year, 'model_id': model.model_id})

    if root is None:
        return None

    for node in root:
        child = Variant.from_xml(node)
        if child:
            variants[child.variant_id] = child

    return variants


def get_variantprice(variant):
    root = web_request('POST', 'variantprice', {'variant_id': variant.variant_id})

    if root is None:
        return None

    assert root.tag.lower() == 'variant'
    variant = Variant.from_xml(root)
    return variant


# def post_vehicle(make, variant, is_new=True):
#     is_new = '1' if is_new else '0'
#
#     root = web_request('POST', 'post-vehicle', {'make': make.make_id,
#                                                 'model': variant.model_id,
#                                                 'year': variant.model_year,
#                                                 'body': variant.body_type_id,
#                                                 'variant': variant.variant_id,
#                                                 'variant_price': variant.list_price_gross,
#                                                 'new_or_used': is_new
#                                                 })
#     return root.get('success', 0) == 1
def get_quote(kms, salary, state, term, variant):
    root = web_request('POST', 'getquote', {'kms': kms,
                                            'price': variant.list_price_gross,
                                            'salary': salary,
                                            'state': state,
                                            'term': term,
                                            'variant_id': variant.variant_id})

    quote = Quote.from_xml(root)
    return quote