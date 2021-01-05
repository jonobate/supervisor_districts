import argparse
import googlemaps
import fiona
from shapely.geometry import shape, Point

API_KEY = ''

if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser()
    
    # Required positional argument
    parser.add_argument('--address', nargs='?', const=1, type=str,
                        default='1260 Mission St, San Francisco, CA 94103')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialise GoogleMaps API connection
    gmaps = googlemaps.Client(key=API_KEY)

    # Geocoding an address
    geocode_result = gmaps.geocode(args.address)
    
    # Get lat long
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    
    # Create point shape from lat long
    point = Point(lng,lat)
    pt = shape(point)
    
    # Import supervisor district shape files
    multipol = fiona.open('districts/geo_export_3a5dacac-ce64-4016-b86a-10fc94d5eab0.shp')
    multis = [m for m in multipol]
    
    # Loop through district shapes, check if point is in shape
    for multi in multis:
        if pt.within(shape(multi['geometry'])):
             print ('%s is in %s' % (args.address, multi['properties']['supdist']))