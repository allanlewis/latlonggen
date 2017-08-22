import csv
import googlemaps
from gooey import Gooey, GooeyParser
from operator import itemgetter
from unidecode import unidecode


@Gooey(program_name='Lat-Lng Generator')
def main():
    parser = GooeyParser()
    parser.add_argument(
        'input_file', widget='FileChooser', metavar='Input file',
        help='A text file containing a list of place names', default='places.txt')
    parser.add_argument(
        'output_file', widget='FileSaver', metavar='Output file',
        help='A CSV file to write the results to', default='places.csv')
    parser.add_argument('api_key', metavar='Google Maps Geocoding API key')
    args = parser.parse_args()

    gmaps = googlemaps.Client(key=args.api_key)
    with open(args.input_file) as input_file, open(args.output_file, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(('Place', 'Latitude', 'Longitude'))
        for place in (unidecode(line.strip()).strip() for line in input_file if not line.startswith('#')):
            try:
                response = gmaps.geocode(place)
                if not response:
                    print(f'No result for {place!r}!')
                    continue

                lat, lng = itemgetter('lat', 'lng')(response[0]['geometry']['location'])
                print(f'{place}: ({lat}, {lng})')
                writer.writerow((place, lat, lng))
            except Exception as exc:
                print(f'Exception while geocoding {place!r}: {exc}')
                continue


if __name__ == '__main__':
    main()
