import requests
from geopy.geocoders import Nominatim
from django.conf import settings

ORS_API_KEY = settings.ORS_API_KEY


# 🔹 CLEAN ADDRESS
def clean_address(address):
    try:
        parts = address.split(",")

        if len(parts) >= 2:
            return parts[-2].strip() + ", Lagos, Nigeria"
        else:
            return address + ", Lagos, Nigeria"

    except:
        return address + ", Lagos, Nigeria"


# 🔹 FAST GEOCODE (NO DELAY)
def geocode_address(address):
    try:
        geolocator = Nominatim(
            user_agent="khasis_express_app",
            timeout=3  # faster timeout
        )

        clean_loc = clean_address(address)

        location = geolocator.geocode(clean_loc)

        if location:
            print(f"📍 {clean_loc} → {location.latitude}, {location.longitude}")
            return [location.longitude, location.latitude]

    except Exception as e:
        print("Geocode error:", e)

    return None


def calculate_distance(pickup, destination):
    try:
        pickup_coords = geocode_address(pickup)
        destination_coords = geocode_address(destination)

        if not pickup_coords or not destination_coords:
            return 0

        url = "https://api.openrouteservice.org/v2/directions/driving-car"

        headers = {
            "Authorization": ORS_API_KEY,
            "Content-Type": "application/json"
        }

        body = {
            "coordinates": [pickup_coords, destination_coords]
        }

        response = requests.post(
            url,
            json=body,
            headers=headers,
            timeout=5
        )

        if response.status_code != 200:
            return 0

        data = response.json()

        return data["routes"][0]["summary"]["distance"] / 1000

    except Exception as e:
        print("Distance error:", e)
        return 0



# 🔹 PRICE FUNCTION (STABLE)
def calculate_price(service_type, distance_km, weight=0):

    try:
        distance_km = float(distance_km)
        weight = float(weight)
    except:
        return 0

    service_type = str(service_type).strip().lower()

    print("SERVICE TYPE:", service_type)

    if service_type == "truck":
        base_price = 7000
        price_per_km = 450
        weight_fee = weight * 360

    elif service_type == "dispatch rider":
        base_price = 1800
        price_per_km = 230
        weight_fee = weight * 195

    elif service_type == "foot courier":
        base_price = 1750
        price_per_km = 285
        weight_fee = weight * 170

    else:
        print("❌ Unknown service type:", service_type)
        return 0

    price = base_price + (distance_km * price_per_km) + weight_fee

    return round(price, 2)