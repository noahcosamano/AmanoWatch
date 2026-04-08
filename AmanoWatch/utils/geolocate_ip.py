import geoip2.database
from pathlib import Path
import ipaddress

DB_PATH = Path(__file__).parent.parent / "utils" / "GeoLite2-Country.mmdb"

# Open once, reuse — Reader is thread-safe and opening per-call is slow
_reader = geoip2.database.Reader(DB_PATH)

def search_ip(ip):
    if not ip:
        return None
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return None
    if addr.is_private or addr.is_loopback or addr.is_link_local:
        return "Private/Local"
    try:
        response = _reader.country(ip)
        name = response.country.name
        return name
    except geoip2.errors.AddressNotFoundError:
        return None