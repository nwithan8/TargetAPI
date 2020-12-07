from typing import Union, List
from urllib.parse import urlencode

import requests

def _make_url(base: str, endpoint: str):
    if base.endswith("/"):
        base = base[:-1]
    if endpoint.startswith("/"):
        endpoint = endpoint[1:]
    return f"{base}/{endpoint}"


class Price:
    def __init__(self, data: dict):
        self._data = data

    @property
    def price(self) -> str:
        return self._data.get('formatted_current_price')

    @property
    def type(self) -> str:
        return self._data.get('formatted_current_price_type')


class OnlineInfo:
    def __init__(self, data: dict):
        self._data = data

    @property
    def availability(self) -> str:
        return self._data.get('availabilityCode')

    @property
    def in_store_pickup(self) -> str:
        return self._data.get('pickUpInStoreStatus')

    @property
    def free_shipping(self) -> bool:
        return self._data.get('freeShipping')


class Promotion:
    def __init__(self, data: dict):
        self._data = data

    @property
    def id(self) -> str:
        return self._data.get('id')

    @property
    def location_id(self) -> str:
        return self._data.get('applied_location_id')

    @property
    def channel(self) -> str:
        return self._data.get('channel')


class Feature:
    def __init__(self, data: dict):
        self._data = data
        self.name = data.get('name')
        self.value = data.get('value')

    def __str__(self):
        return f"{self.name} {self.value}"


class Store:
    def __init__(self, data: dict, target):
        self._data = data
        self._target_instance = target

    @property
    def id(self) -> str:
        return self._data.get('location_id')

    @property
    def name(self) -> str:
        return self._data.get('location_name')

    @property
    def type(self) -> str:
        return self._data.get('location_type')

    @property
    def address(self) -> str:
        return self._data.get('address_line_1')

    @property
    def city(self) -> str:
        return self._data.get('city')

    @property
    def region(self) -> str:
        return self._data.get('region')

    @property
    def zipcode(self) -> str:
        return self._data.get('postal_code')

    @property
    def latitude(self) -> str:
        return self._data.get('latitude')

    @property
    def longitude(self) -> str:
        return self._data.get('longitude')

    @property
    def active(self) -> str:
        return self._data.get('is_active')

    @property
    def obgd_enabled(self) -> str:
        return self._data.get('obgd_enabled')


class AvailabilityLocation(Store):
    def __init__(self, data: dict, target):
        self._data = data
        self._target_instance = target
        self._make_store()

    def _make_store(self):
        temp_store = self._target_instance._store_by_id(store_id=self._data.get('location_id'))
        super().__init__(data=temp_store._data, target=self._target_instance)
        del temp_store

    @property
    def onhand(self) -> int:
        return self._data.get('onhand_quantity')

    @property
    def demand(self) -> str:
        return self._data.get('location_demand_sum')

    @property
    def hard_demand(self) -> str:
        return self._data.get('location_hard_demand_sum')

    @property
    def soft_demand(self) -> str:
        return self._data.get('location_soft_demand_sum')

    @property
    def reserve(self) -> str:
        return self._data.get('product_location_reserve')

    @property
    def walk_in_reserve(self) -> str:
        return self._data.get('product_location_pickup_walkin_reserve')

    @property
    def status(self) -> str:
        return self._data.get('availability_status')


class Availability:
    def __init__(self, data: dict, target, product):
        self._data = data
        self._target_instance = target
        self._product = product

    def __str__(self):
        return f"{self._data.get('availability')} - {self._data.get('availability_status')}"

    @property
    def limited_quantity(self) -> bool:
        return self._data.get('limited_quantity_enabled')

    @property
    def total_quantity(self) -> bool:
        return self._data.get('available_to_promise_quantity')

    @property
    def online_quantity(self) -> bool:
        return self._data.get('online_available_to_promise_quantity')

    @property
    def in_store_quantity(self) -> bool:
        return self._data.get('stores_available_to_promise_quantity')

    @property
    def preorder_quantity(self) -> bool:
        return self._data.get('pre_order_available_to_promise_quantity')

    @property
    def locations(self) -> List[AvailabilityLocation]:
        locations = []
        for loc in self._data.get('locations', []):
            locations.append(AvailabilityLocation(data=loc, target=self._target_instance))
        return locations

class Product:
    def __init__(self, data: dict, target, store = None):
        self._data = data
        self._target_instance = target
        self.store = store

    @property
    def details(self) -> dict:
        return self._target_instance.redsky.get_product_details()

    @property
    def availability(self) -> dict:
        return self._target_instance.api.product_availability(product=self)

    @property
    def dcpi(self) -> str:
        return self._data.get('dcpi')

    @property
    def tcin(self) -> str:
        return self._data.get('tcin')

    @property
    def unit_term(self) -> str:
        return self._data.get('buyUnitOfMeasure')

    @property
    def upc(self) -> str:
        return self._data.get('upc')

    @property
    def name(self) -> str:
        return self._data.get('title')

    @property
    def description(self) -> str:
        return self._data.get('description')

    @property
    def state(self) -> str:
        return self._data.get('itemState')

    @property
    def type(self) -> str:
        return self._data.get('itemType')

    @property
    def price(self) -> Union[Price, None]:
        if self._data.get('price'):
            return Price(data=self._data.get('price'))
        return None

    @property
    def online(self) -> Union[OnlineInfo, None]:
        if self._data.get('onlineInfo'):
            return OnlineInfo(data=self._data.get('onlineInfo'))
        return None

    @property
    def promotions(self) -> List[Promotion]:
        if not self._data.get('promotions'):
            return []
        return [Promotion(data=promo) for promo in self._data.get('promotions')]

    @property
    def features(self) -> List[Feature]:
        if not self._data.get('features'):
            return []
        return [Feature(data=feature) for feature in self._data.get('features')]


class Target:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self.api = TargetAPI(api_key=api_key, target_instance=self)
        self.redsky = RedSky(api_key=api_key, target_instance=self)

    def _store_by_id(self, store_id: str) -> Union[Store, None]:
        for store in self.stores:
            if store.id == store_id:
                return store
        return None

    def find_stores(self, keyword: str) -> List[Store]:
        locations = []
        for store in self.stores:
            if keyword in store.name:
                locations.append(store)
        return locations

    @property
    def stores(self) -> List[Store]:
        return self.api.stores

    def search(self, keyword: str, store_id: str = None, store_search: bool = False, sort_by: str = "relevance") -> List[Product]:
        return self.redsky.search_products(keyword=keyword, store_id=store_id, store_search=store_search, sort_by=sort_by)


class API:
    def __init__(self, api_key: str, target_instance: Target):
        self._key = api_key
        self._target_instance = target_instance
        self._base_url = "https://api.target.com/"

    def _get_json(self, endpoint: str, params: dict = {}) -> dict:
        res = self._get(endpoint=endpoint, params=params)
        if res:
            return res.json()
        return {}

    def _get(self, endpoint: str, params: dict = {}) -> Union[requests.Response, None]:
        params['key'] = self._key
        url = _make_url(base=self._base_url, endpoint=endpoint)
        url += f"?{urlencode(params)}"
        print(url)
        res = requests.get(url=url)
        if res:
            return res
        return None


class RedSky(API):
    def __init__(self, api_key: str, target_instance: Target):
        super().__init__(api_key=api_key, target_instance=target_instance)
        self._base_url = "https://redsky.target.com/"

    def search_products(self, keyword: str, store_id: str = None, store_search: bool = False, sort_by: str = "relevance") -> List[Product]:
        products = []
        params = {
            'searchTerm': keyword,
            'pageNumber': 1,
            'storeSearch': store_search,
            'sortBy': sort_by,
            'pricing_context': 'digital' if not store_id else 'in_store',
            'pricing_store_id': store_id if store_id else '3991'
        }
        endpoint = 'v4/products/list'
        if store_id:
            endpoint += f"/{store_id}"
            params['storeId'] = store_id
        data = self._get_json(endpoint=endpoint, params=params)
        if data:
            if not data.get('products'):
                print("Target is attempting to redirect you to a category page. Please reword your keyword.")
            else:
                for prod in data['products']:
                    products.append(Product(data=prod, target=self._target_instance))
        return products



class TargetAPI(API):
    def __init__(self, api_key: str, target_instance: Target):
        super().__init__(api_key=api_key, target_instance=target_instance)
        self._base_url = "https://api.target.com/"
        self._locations = []

    @property
    def stores(self) -> List[Store]:
        if not self._locations:
            self._locations = []
            data = self._get_json(endpoint='ship_locations/v1')
            if data:
                for loc in data:
                    self._locations.append(Store(data=loc, target=self._target_instance))
        return self._locations

    def product_availability(self, product: Product, nearby_store: str = None, inventory_type: str = 'ALL', multichannel: str = 'ALL') -> Union[Availability, None]:
        params = {
            'inventory_type': inventory_type,
            'multichannel_option': multichannel
        }
        if nearby_store:
            params['nearby_store'] = nearby_store
        data = self._get_json(endpoint=f"available_to_promise/v2/{product.tcin}", params=params)
        if data and data.get('products'):
            return Availability(data=data['products'][0], target=self._target_instance, product=product)
        return None