from typing import Union, List

from TargetAPI.stores import AvailabilityLocation

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