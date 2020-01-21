import json, math
import requests


class Stores:
    def __init__(self):
        # Read all stores along with their postcodes
        with open("stores.json", "r") as f:
            contents = f.read()
        self.stores = json.loads(contents)

    @classmethod
    def _postcode_to_location(self, postcode):
        url = "http://api.postcodes.io/postcodes/%s" % postcode
        ret = requests.get(url)
        status = ret.status_code
        if status != 200:
            print("Bad response: %d for url %s" % (status, url))
            return None
        text = json.loads(ret.text)
        return text["result"]

    def sort_by_name(self):
        # Sort the stores according to alphabetical order
        return sorted(self.stores, key=lambda x: x["name"])

    def populate_location_info(self):
        # Append location information for each postcode using the postcode.io service apis
        for store in self.stores:
            # Fetch the location from a postcode
            location = self._postcode_to_location(store["postcode"])
            if not location:
                continue
            # Include the standard lat/long
            store["latitude"] = location["latitude"]
            store["longitude"] = location["longitude"]
            # Along with the National Grid coords for easy calculating of distances
            store["eastings"] = location["eastings"]
            store["northings"] = location["northings"]

    def stores_around_postcode(self, postcode, distance):
        # Return a list of stores which are located within distance (in metres) of a postcode
        location = self._postcode_to_location(postcode)
        results = []
        for store in self.stores:
            if not ("eastings" in store and "northings" in store):
                continue
            dx = abs(store["eastings"] - location["eastings"])
            dy = abs(store["northings"] - location["northings"])
            d = math.sqrt(dx * dx + dy * dy)
            if d <= distance:
                results.append(store)
        # Return the results in northings descending order
        results.sort(key=lambda x: x["northings"], reverse=True)
        return results
