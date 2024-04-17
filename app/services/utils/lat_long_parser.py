import re


def extract_coordinates(url):
    '''
    Method to extract coordinates from a Google Maps URL
    :param url:
    :return:
    '''
    if not "https://www" in url:
        latitude, longitude = url.strip().split(",")
        return [float(latitude), float(longitude)]
    pattern = r'@([-\d.]+),([-\d.]+)'
    match = re.search(pattern, url)
    if match:
        latitude, longitude = match.groups()
        return [float(latitude), float(longitude)]
    else:
        return None