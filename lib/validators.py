"""
Input data should be validated, for our services what can be validated before further process,
are Latitudes and longitudes
"""
def latlng_validate(latlng):
    try:
        # Latitudes range from -90 to 90, and longitudes range from -180 to 80
        lat, lng = (float(item) for item in latlng.split(','))
        if lat < -90 or lat > 90:
            return False
        if lng < -180 or lng > 80:
            return False

        return True
    except:
        return False
