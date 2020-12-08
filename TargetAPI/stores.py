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

    @property
    def phone_number(self) -> str:
        return self._data.get('phone')

    def search(self, keyword: str, store_search: bool = False, sort_by: str = "relevance"):
        return self._target_instance.redsky.search_products(keyword=keyword, store_id=self.id, store_search=store_search, sort_by=sort_by)


class AvailabilityLocation:
    def __init__(self, data: dict, target):
        self._data = data
        self._target_instance = target
        self.store = self._target_instance._store_by_id(store_id=self._data.get('location_id'))

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