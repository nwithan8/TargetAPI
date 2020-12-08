# TargetAPI
Interact with Target's API

# Installation
Download from PyPi with ``pip install TargetAPI``

# Usage
- Import with ``from TargetAPI import Target``
- Initialize with ``target = Target(api_key="myapikeyhere")``

Examples:
- Get stores: ``stores = target.stores``
- Search for a product: ``results = target.search(keyword="PlayStation 5 game console")``
- Product availability: ``availability = results[0].availability``
- Availability locations: ``locations = availability.locations``
- Location phone number: ``print(locations[0].store.phone_number)``
