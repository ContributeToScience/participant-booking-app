from django.conf import settings
from .ip2geo import GeoIP, MEMORY_CACHE

geoip = GeoIP(settings.MAXMIND_CITY_DB_PATH, MEMORY_CACHE)