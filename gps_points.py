import osmnx as ox
import random


class GPSPoints:

    def __init__(self, city_name: str, num_points: int = 25):
        self.city_name = city_name
        self.gps_points = self.fetch_road_gps_points(num_points)

    def fetch_road_gps_points(self, num_points: int) -> list[tuple[float, float]]:
        g = ox.graph_from_place(self.city_name, network_type='drive')
        nodes = list(g.nodes())
        selected_nodes = random.sample(nodes, num_points)
        gps_points = [(g.nodes[node]['y'], g.nodes[node]['x']) for node in selected_nodes]
        return gps_points
