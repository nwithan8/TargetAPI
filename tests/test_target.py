import TargetAPI
from TargetAPI.models import SearchProduct, StoreProductChild
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


def test_product_availability_with_store():
    target: TargetAPI.Target = client()
    product_data = {
        'tcin': '83971257',
    }
    product = TargetAPI.models.SearchProduct(**product_data)
    store_data = {
        'location_id': 1928,
    }
    store = TargetAPI.models.Location(**store_data)
    in_store_product: StoreProductChild = target.redsky.product_availability_at_store(product=product, store=store)
    assert in_store_product is not None
    price = in_store_product.price
    assert price is not None
