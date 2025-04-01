import os
from typing import List, Tuple, Optional, Dict

import aiohttp
import asyncio

NEARBY_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

async def search_nearby_places(location: Tuple[float, float],
                               radius: float,
                               place_type: Optional[str] = None,
                               require_photo: bool = False,
                               max_results: int = 20) -> List[Dict]:
    """
    Asynchronously search for nearby places around a given location within a specified radius
    using the Google Places Nearby Search API. This function returns a filtered dictionary
    for each candidate with fields relevant for market research:
    business_status, name, place_id, opening_hours, rating, type, user_ratings_total,
    vicinity, price_level, photos, geometry (location), permanently_closed.
    
    Args:
        location (Tuple[float, float]): (latitude, longitude).
        radius (float): Search radius in kilometers.
        place_type (Optional[str]): Filter by the specified place type (if provided).
        require_photo (bool): If True, only returns results that include a photo.
        max_results (int): Maximum number of results to return. Default is 20.
    
    Returns:
        List[Dict]: A list of dictionaries (one per candidate) with market research relevant fields.
    
    Raises:
        Exception: If the API request fails.
    """
    params = {
        "location": f"{location[0]},{location[1]}",
        "radius": int(radius * 1000),
        "key": os.environ["GOOGLE_MAPS_API_KEY"]
    }
    if place_type:
        params["type"] = place_type

    all_results = []
    next_page_token = None

    async with aiohttp.ClientSession() as session:
        while len(all_results) < max_results:
            if next_page_token:
                # Wait for 2 seconds before requesting the next page (Google's requirement)
                await asyncio.sleep(2)
                params["pagetoken"] = next_page_token
            else:
                params.pop("pagetoken", None)

            async with session.get(NEARBY_SEARCH_URL, params=params) as response:
                response_data = await response.json()

            status = response_data.get("status")
            if status not in ("OK", "ZERO_RESULTS"):
                raise Exception(f"Error fetching place data: {status}")
            
            raw_candidates = response_data.get("results", [])
            if require_photo:
                raw_candidates = [c for c in raw_candidates if c.get("photos")]

            for candidate in raw_candidates:
                if len(all_results) >= max_results:
                    break
                    
                # Extract opening hours information
                opening_hours = candidate.get("opening_hours", {})
                is_open_now = opening_hours.get("open_now", False)
                
                # Extract location information
                geometry = candidate.get("geometry", {})
                location = geometry.get("location", {})
                
                mapped = {
                    "business_status": candidate.get("business_status"),
                    "name": candidate.get("name"),
                    "place_id": candidate.get("place_id"),
                    "is_open_now": is_open_now,
                    "rating": candidate.get("rating"),
                    "type": candidate.get("types", []),
                    "user_ratings_total": candidate.get("user_ratings_total"),
                    "type_string": ", ".join(candidate.get("types", [])),
                    "vicinity": candidate.get("vicinity"),
                    "price_level": candidate.get("price_level", 0),  # 0 means not available
                    "has_photos": bool(candidate.get("photos")),
                    "latitude": location.get("lat"),
                    "longitude": location.get("lng"),
                    "permanently_closed": candidate.get("permanently_closed", False),
                    "price_level_symbols": "💰" * (candidate.get("price_level", 0) or 0)  # For visualization
                }
                all_results.append(mapped)

            next_page_token = response_data.get("next_page_token")
            if not next_page_token:
                break

    return all_results

# Example usage:
async def main():
    center_location = (13.0196719, 80.2688418)
    search_radius_km = 2.0
    try:
        # Example: search for "restaurant" type results
        candidates = await search_nearby_places(center_location, search_radius_km, "restaurant", require_photo=True, max_results=40)
        for cand in candidates:
            print(f"Name: {cand.get('name')}, Vicinity: {cand.get('vicinity')}")
    except Exception as e:
        print(f"Error occurred: {e}")

# To run the example, uncomment the following line:
# asyncio.run(main())