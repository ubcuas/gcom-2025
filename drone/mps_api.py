import requests
import json

class DroneApiClient:
    _mission_planner_api_url = "http://localhost:9001"

    @staticmethod
    def _fetch_from_mission_planner(endpoint, method="GET", data=None):
        url = f"{DroneApiClient._mission_planner_api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=json.dumps(data))
        return response

    @staticmethod
    def get_current_status():
        return DroneApiClient._fetch_from_mission_planner("status")

    @staticmethod
    def get_status_history():
        return DroneApiClient._fetch_from_mission_planner("status/history")

    @staticmethod
    def takeoff(altitude):
        return DroneApiClient._fetch_from_mission_planner("drone/takeoff", method="POST", data={"altitude": altitude})

    @staticmethod
    def arm(arm_value):
        return DroneApiClient._fetch_from_mission_planner("drone/arm", method="POST", data={"arm": arm_value})

    @staticmethod
    def land():
        return DroneApiClient._fetch_from_mission_planner("drone/land")

    @staticmethod
    def rtl(altitude):
        return DroneApiClient._fetch_from_mission_planner("drone/rtl", method="POST", data={"altitude": altitude})

    @staticmethod
    def lock():
        return DroneApiClient._fetch_from_mission_planner("drone/lock")

    @staticmethod
    def unlock():
        return DroneApiClient._fetch_from_mission_planner("drone/unlock")

    @staticmethod
    def get_queue():
        return DroneApiClient._fetch_from_mission_planner("drone/queue")

    @staticmethod 
    def post_queue(queue):
        return DroneApiClient._fetch_from_mission_planner("drone/queue", method="POST", data=queue)

    @staticmethod
    def post_home(wp):
        return DroneApiClient._fetch_from_mission_planner("drone/home", method="POST", data=wp)
