class GoogleMapsClient:
    def get_directions(self, origin: str, dest: str):
        return {"route": f"{origin} -> {dest}", "distance_km": 10.0}
