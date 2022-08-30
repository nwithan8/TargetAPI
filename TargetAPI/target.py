from typing import Union, List
from urllib.parse import urlencode

import requests

from TargetAPI.models import SearchResults, OnlineAvailabilityResults, OnlineProduct, \
    StoreAvailabilityResults, StoreProduct, StoreProductChild, SearchProduct, Location


def _make_url(base: str, endpoint: str):
    if base.endswith("/"):
        base = base[:-1]
    if endpoint.startswith("/"):
        endpoint = endpoint[1:]
    return f"{base}/{endpoint}"


class Target:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self.api = TargetAPI(api_key=api_key, target_instance=self)
        self.redsky = RedSky(api_key=api_key, target_instance=self)

    def _store_by_id(self, store_id: str) -> Union[Location, None]:
        for store in self.stores:
            if store.location_id == store_id:
                return store
        return None

    def find_stores(self, keyword: str) -> List[Location]:
        locations = []
        for store in self.stores:
            if keyword in store.location_name:
                locations.append(store)
        return locations

    @property
    def stores(self) -> List[Location]:
        return self.api.stores

    def search(self, keyword: str, store_id: str = None, store_search: bool = False, sort_by: str = "relevance") \
            -> List[SearchProduct]:
        return self.redsky.search_products(keyword=keyword, store_id=store_id, store_search=store_search,
                                           sort_by=sort_by)


class API:
    def __init__(self, api_key: str, target_instance: Target):
        self._key = api_key
        self._target_instance = target_instance
        self._base_url = "https://api.target.com/"
        self._session = requests.Session()

    def _get_json(self, endpoint: str, params: dict = {}) -> dict:
        res = self._get(endpoint=endpoint, params=params)
        if res:
            return res.json()
        return {}

    def _get(self, endpoint: str, params: dict = {}) -> Union[requests.Response, None]:
        params['key'] = self._key
        url = _make_url(base=self._base_url, endpoint=endpoint)
        url += f"?{urlencode(params)}"
        res = self._session.get(url=url)
        if res:
            return res
        return None


class RedSky(API):
    def __init__(self, api_key: str, target_instance: Target):
        super().__init__(api_key=api_key, target_instance=target_instance)
        self._base_url = "https://redsky.target.com/"

    def _search(self, endpoint: str, **kwargs):
        params = {
            'channel': 'WEB',
            'page': '/s/none',
            'visitor_id': 1,
            'is_bot': False,
        }
        params.update(kwargs)
        return self._get_json(endpoint=endpoint, params=params)

    def search_products(self, keyword: str, store_id: str = None, store_search: bool = False,
                        sort_by: str = "relevance") -> List[SearchProduct]:
        params = {
            'keyword': keyword,
            'pricing_store_id': store_id if store_id else 1928,
            'pageNumber': 1,
            'storeSearch': store_search,
            'sortBy': sort_by,
            'pricing_context': 'digital' if not store_id else 'in_store',
        }
        data = self._search(endpoint='redsky_aggregations/v1/web/plp_search_v1', **params)
        if data:
            return SearchResults(**data).data.search.products
        return []

    def product_availability(self, product: SearchProduct) -> Union[OnlineProduct, None]:
        params = {
            'tcin': product.tcin,
            'pricing_context': 'digital',
            'pricing_store_id': 1928,  # default value
        }
        data = self._search(endpoint='redsky_aggregations/v1/web_platform/product_fulfillment_v1', **params)
        if data:
            availability_results = OnlineAvailabilityResults(**data)
            return availability_results.data.product
        return None

    def product_availability_at_store(self, product: SearchProduct, store: Location) -> Union[StoreProduct, StoreProductChild, None]:
        params = {
            'tcin': product.tcin,
            'pricing_context': 'in_store',
            'store_id': store.location_id,
            'pricing_store_id': store.location_id,
            'has_pricing_store_id': True,
            'scheduled_delivery_store_id': store.location_id,
        }
        data = self._search(endpoint='redsky_aggregations/v1/web/pdp_client_v1', **params)
        if data:
            availability_results = StoreAvailabilityResults(**data)
            if availability_results.data.product.tcin == product.tcin:
                return availability_results.data.product
            for child in availability_results.data.product.children:
                if child.tcin == product.tcin:
                    return child
        return None


class TargetAPI(API):
    def __init__(self, api_key: str, target_instance: Target):
        super().__init__(api_key=api_key, target_instance=target_instance)
        self._base_url = "https://api.target.com/"
        self._locations = []

    @property
    def locations(self) -> List[Location]:
        if not self._locations:
            self._locations = []
            data = self._get_json(endpoint='ship_locations/v1')
            if data:
                for loc in data:
                    self._locations.append(Location(**loc))
        return self._locations

    @property
    def stores(self) -> List[Location]:
        locations = []
        for location in self.locations:
            if location.location_type == "STORE":
                locations.append(location)
        return locations

    @property
    def vendors(self) -> List[Location]:
        locations = []
        for location in self.locations:
            if location.location_type == "VENDOR":
                locations.append(location)
        return locations

    @property
    def sellers(self) -> List[Location]:
        locations = []
        for location in self.locations:
            if location.location_type == "SELLER_LOCATION":
                locations.append(location)
        return locations
