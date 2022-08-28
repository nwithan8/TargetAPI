import TargetAPI
from tests.setup import client


def test_stores():
    target: TargetAPI.Target = client()
    stores = target.api.stores
    assert stores is not None


def test_search():
    target: TargetAPI.Target = client()
    results = target.search(keyword="iphone")
    assert results is not None


def test_product_availability():
    target: TargetAPI.Target = client()
    results = target.search(keyword="iphone")
    assert results is not None
    product = results[0]
    assert product is not None
    availability = target.redsky.product_availability(product=product)
    assert availability is not None
