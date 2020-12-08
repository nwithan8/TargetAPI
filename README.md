# TargetAPI
Interact with Target's API

# Installation
Download from PyPi with ``pip install TargetAPI``
https://pypi.org/project/TargetAPI/

# Usage
- Import with ``from TargetAPI import Target``
- Initialize with ``target = Target(api_key="myapikeyhere")``

Examples:
- Get stores: ``stores = target.stores``
- Search for a product: ``results = target.search(keyword="PlayStation 5 game console")``
- Product reviews: ``reviews = results[0].reviews``
- Product price: ``price = results[0].price``
- Product availability: ``availability = results[0].availability``
- Products on-hand: ``print(availability.onhand)``
- Availability locations: ``locations = availability.locations``
- Location phone number: ``print(locations[0].store.phone_number)``


# Credits
Thanks to @MichaelPriebe for his myStore app source code, which helped me determine the proper API endpoints

# Contact
Please leave a pull request if you would like to contribute.

Follow me on Twitter: [@nwithan8](https://twitter.com/nwithan8)

Also feel free to check out my other projects here on [GitHub](https://github.com/nwithan8) or join the #developer channel in my Discord server below.

<div align="center">
	<p>
		<a href="https://discord.gg/ygRDVE9"><img src="https://discordapp.com/api/guilds/472537215457689601/widget.png?style=banner2" alt="" /></a>
	</p>
</div>
