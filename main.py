from utils import find_central_point, get_city_name
from gps_points import GPSPoints
from genetic_route_planning import GeneticRoutePlanning


def main(towns_gps_points: list[GPSPoints]):
    # Level 1: Inter-town optimization
    town_central_points = [find_central_point(town.gps_points) for town in towns_gps_points]
    best_inter_town_route_indices, min_distance = GeneticRoutePlanning(town_central_points).run_ga()
    best_inter_town_route = [{"GPS points": town_central_points[i], "City_Name": get_city_name(town_central_points[i][0], town_central_points[i][1])} for i in best_inter_town_route_indices]

    # Level 2: Intra-town optimization
    best_intra_town_routes = {}
    best_inter_town_route_with_city_name = []
    for i, town_index in enumerate(best_inter_town_route_indices):
        town_gps_points = towns_gps_points[town_index]
        best_inter_town_route_with_city_name.append({"GPS points": best_inter_town_route_indices[i], "City Name": town_gps_points.city_name})
        best_route, min_distance_intra_town = GeneticRoutePlanning(town_gps_points.gps_points).run_ga()
        best_intra_town_routes[town_central_points[town_index]] = {}
        best_intra_town_routes[town_central_points[town_index]]["GPS points"] = [town_gps_points.gps_points[i] for i in best_route]
        best_intra_town_routes[town_central_points[town_index]]["Distance"] = min_distance_intra_town
        best_intra_town_routes[town_central_points[town_index]]["Town name"] = town_gps_points.city_name

    return best_inter_town_route_indices, best_intra_town_routes, min_distance


if __name__ == "__main__":
    # Fetch road GPS points for a specific area
    area_names = ["Malibu", "Los Angeles", "Long Beach", "Torrance"]
    gps_points = []
    for area in area_names:
        gps_points.append(GPSPoints(area))

    # Run the genetic algorithm with these road GPS points
    best_inter_town, best_intra_town, min_distance = main(gps_points)
    print("Best Inter-Town Route:", best_inter_town)
    print("Distance:", min_distance, "km")
    print("Best Intra-Town Routes:", best_intra_town)