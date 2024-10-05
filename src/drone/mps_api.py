import requests
import json


class DroneApiClient:
    _mission_planner_api_url = "http://localhost:9001"

    @staticmethod
    def _fetch_from_mission_planner(endpoint, method="GET", data=None):
        url = f"{DroneApiClient._mission_planner_api_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
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
        return DroneApiClient._fetch_from_mission_planner(
            "takeoff", method="POST", data={"altitude": altitude}
        )

    @staticmethod
    def arm(arm_value):
        return DroneApiClient._fetch_from_mission_planner(
            "arm", method="POST", data={"arm": arm_value}
        )

    @staticmethod
    def land():
        return DroneApiClient._fetch_from_mission_planner("land")

    @staticmethod
    def get_rlt():
        return DroneApiClient._fetch_from_mission_planner("rtl")

    @staticmethod
    def post_rtl(altitude):
        return DroneApiClient._fetch_from_mission_planner(
            "rtl", method="POST", data={"altitude": altitude}
        )

    @staticmethod
    def lock():
        return DroneApiClient._fetch_from_mission_planner("lock")

    @staticmethod
    def unlock():
        return DroneApiClient._fetch_from_mission_planner("unlock")

    @staticmethod
    def get_queue():
        return DroneApiClient._fetch_from_mission_planner("queue")

    @staticmethod
    def post_queue(queue):
        return DroneApiClient._fetch_from_mission_planner(
            "queue", method="POST", data=queue
        )

    @staticmethod
    def post_home(wp):
        return DroneApiClient._fetch_from_mission_planner(
            "home", method="POST", data=wp
        )

    @staticmethod
    def prepend(wp):
        return DroneApiClient._fetch_from_mission_planner(
            "prepend", method="POST", data=wp
        )

    @staticmethod
    def append(wp):
        return DroneApiClient._fetch_from_mission_planner(
            "append", method="POST", data=wp
        )

    @staticmethod
    def clear():
        return DroneApiClient._fetch_from_mission_planner("clear")

    @staticmethod
    def diversion(exclude_wps, rejoin_wp):
        return DroneApiClient._fetch_from_mission_planner(
            "diversion",
            method="POST",
            data={"exclude": exclude_wps, "rejoin_at": rejoin_wp},
        )

    @staticmethod
    def get_vtol_transition():
        return DroneApiClient._fetch_from_mission_planner("vtol/transition")

    @staticmethod
    def post_vtol_transition(mode):
        return DroneApiClient._fetch_from_mission_planner(
            "vtol/transition", method="POST", data={"mode": mode}
        )

    @staticmethod
    def flightmode(mode):
        return DroneApiClient._fetch_from_mission_planner(
            "flightmode", method="POST", data={"mode": mode}
        )
