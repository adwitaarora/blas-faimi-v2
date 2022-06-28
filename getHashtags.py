import geocoder
def get_trends(api, loc):
    # Object that has location's latitude and longitude.
    g = geocoder.osm(loc)

    closest_loc = api.closest_trends(g.lat, g.lng)
    trends = api.get_place_trends(closest_loc[0]["woeid"])
    return trends[0]["trends"]

