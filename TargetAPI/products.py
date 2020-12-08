from typing import Union, List
from datetime import datetime

from TargetAPI.stores import AvailabilityLocation
import TargetAPI.helpers as helpers

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

    @property
    def message(self) -> str:
        return self._data.get('pdp_message')


class Feature:
    def __init__(self, data: dict):
        self._data = data
        self.name = data.get('name')
        self.value = data.get('value')

    def __str__(self):
        return f"{self.name} {self.value}"

class Video:
    def __init__(self, data: dict):
        self._data = data

    @property
    def title(self) -> str:
        return self._data.get("video_title")

    @property
    def links(self) -> List[str]:
        return [file.get('video_url') for file in self._data.get('video_files')]

class Availability:
    def __init__(self, data: dict, target, product):
        self._data = data
        self._target_instance = target
        self._product = product

    def __str__(self):
        return f"{self._data.get('availability')} - {self._data.get('availability_status')}"

    @property
    def availability(self) -> str:
        return self.__str__()

    @property
    def limited_quantity(self) -> bool:
        return self._data.get('limited_quantity_enabled')

    @property
    def total_quantity(self) -> int:
        return self._data.get('available_to_promise_quantity')

    @property
    def online_quantity(self) -> int:
        return self._data.get('online_available_to_promise_quantity')

    @property
    def in_store_quantity(self) -> int:
        return self._data.get('stores_available_to_promise_quantity')

    @property
    def preorder_quantity(self) -> int:
        return self._data.get('pre_order_available_to_promise_quantity')

    @property
    def locations(self) -> List[AvailabilityLocation]:
        locations = []
        for loc in self._data.get('locations', []):
            locations.append(AvailabilityLocation(data=loc, target=self._target_instance))
        return locations

    @property
    def release_date(self) -> datetime:
        return helpers.string_to_datetime(date_string=self._data.get('release_date'))

    @property
    def available_to_purchase_date(self) -> datetime:
        return helpers.string_to_datetime(date_string=self._data.get('available_to_purchase_date_time'))

    @property
    def back_order_start_date(self) -> datetime:
        return helpers.string_to_datetime(date_string=self._data.get('back_order_start_date'))

    @property
    def back_order_end_date(self) -> datetime:
        return helpers.string_to_datetime(date_string=self._data.get('back_order_end_date'))


class Review:
    def __init__(self, data: dict):
        self._data = data

    @property
    def title(self) -> str:
        return self._data.get('title')

    @property
    def submitted_at(self) -> datetime:
        return helpers.string_to_datetime(date_string=self._data.get('submissionTime'), template="%Y-%m-%dT%H:%M:%S+0000")

    @property
    def text(self) -> str:
        return self._data.get('reviewText')

    @property
    def rating(self) -> int:
        return self._data.get('rating')

    @property
    def feedback_count(self) -> int:
        return self._data.get('totalFeedbackCount')

    @property
    def upvotes(self) -> int:
        return self._data.get('totalPositiveFeedbackCount')

    @property
    def type(self) -> str:
        return self._data.get('reviewType')


class ReviewSummary:
    def __init__(self, data: dict):
        self._data = data

    @property
    def count(self) -> int:
        return self._data.get('guestReviewCount')

    @property
    def average(self) -> float:
        return self._data.get('overallGuestRating')

    @property
    def most_helpful(self) -> List[Review]:
        reviews = []
        for review in self._data.get('mostHelpfulReviews'):
            reviews.append(Review(data=review))
        return reviews

    @property
    def stars(self) -> dict:
        return self._data.get('ratingDistribution')


class Product:
    def __init__(self, data: dict, target, store = None):
        self._data = data
        self._target_instance = target
        self.store = store

    @property
    def details(self) -> dict:
        return self._target_instance.redsky.get_product_details()

    @property
    def availability(self) -> Availability:
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

    @property
    def highlights(self) -> List[str]:
        if self._data.get('softBullets'):
            return self._data['softBullets'].get('bullets')
        return []

    @property
    def channels(self) -> str:
        return self._data.get('channelAvailabilityCode')

    @property
    def reviews(self) -> ReviewSummary:
        return ReviewSummary(data=self._data.get('guestReviews'))

    @property
    def has_recall(self) -> bool:
        return self._data.get('recallExists', False)

    @property
    def can_buy(self) -> bool:
        return self._data.get('isBuyable', False)

    @property
    def store_pickup(self) -> bool:
        return self._data.get('isPickUpFromStoreEligible', False)

    @property
    def ship_from_store(self) -> bool:
        return self._data.get('isShipFromStoreEligible', False)

    @property
    def return_policy(self) -> str:
        return self._data.get('returnPolicy')

    @property
    def image(self) -> str:
        if self._data.get('images'):
            return self._data['images'].get('primaryUri')
        return ""

    @property
    def videos(self) -> List[Video]:
        videos = []
        for vid in self._data.get('videos'):
            videos.append(Video(data=vid))
        return videos

    @property
    def brand(self) -> str:
        return self._data.get('manufacturingBrand')

    @property
    def link(self) -> str:
        return self._data.get('targetDotComUri')

    @property
    def max_allowed(self) -> int:
        return self._data.get('maxAllowedQuantity')

    @property
    def weight(self) -> str:
        if self._data.get('package_dimensions'):
            return f"{self._data['package_dimensions'].get('weight')} {self._data['package_dimensions'].get('weight_unit_of_measure')}"
        return ""

    @property
    def launch_date(self) -> datetime:
        return helpers.string_to_datetime(date_string=self._data.get('launchDate'), template="%Y-%m-%dT%H:%M:%S+0000")
