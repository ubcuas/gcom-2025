import requests
import json


class DroneApiClient:
    _mission_planner_api_url = "http://localhost:9000"

    @staticmethod
    def _mission_planner_api_call(endpoint, method="GET", data=None):
        response = None
        url = f"{DroneApiClient._mission_planner_api_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=json.dumps(data))
        return response

    @staticmethod
    def get_current_status():
        return DroneApiClient._mission_planner_api_call("status")

    @staticmethod
    def get_status_history():
        return DroneApiClient._mission_planner_api_call("status/history")

    @staticmethod
    def takeoff(altitude):
        return DroneApiClient._mission_planner_api_call(
            "takeoff", method="POST", data={"altitude": altitude}
        )

    @staticmethod
    def arm(arm_value):
        return DroneApiClient._mission_planner_api_call(
            "arm", method="PUT", data={"arm": arm_value}
        )

    @staticmethod
    def land():
        return DroneApiClient._mission_planner_api_call("land")

    @staticmethod
    def get_rlt():
        return DroneApiClient._mission_planner_api_call("rtl")

    @staticmethod
    def post_rtl(altitude):
        return DroneApiClient._mission_planner_api_call(
            "rtl", method="POST", data={"altitude": altitude}
        )

    @staticmethod
    def lock():
        return DroneApiClient._mission_planner_api_call("lock")

    @staticmethod
    def unlock():
        return DroneApiClient._mission_planner_api_call("unlock")

    @staticmethod
    def get_queue():
        return DroneApiClient._mission_planner_api_call("queue")

    @staticmethod
    def post_queue(queue):
        return DroneApiClient._mission_planner_api_call(
            "queue", method="POST", data=queue
        )

    @staticmethod
    def post_home(wp):
        return DroneApiClient._mission_planner_api_call("home", method="POST", data=wp)

    @staticmethod
    def insert(queue):
        return DroneApiClient._mission_planner_api_call(
            "insert", method="POST", data=queue
        )

    @staticmethod
    def clear():
        return DroneApiClient._mission_planner_api_call("clear")

    @staticmethod
    def diversion(exclude_wps, rejoin_wp):
        return DroneApiClient._mission_planner_api_call(
            "diversion",
            method="POST",
            data={"exclude": exclude_wps, "rejoin_at": rejoin_wp},
        )

    @staticmethod
    def flightmode(mode):
        return DroneApiClient._mission_planner_api_call(
            "flightmode", method="POST", data={"mode": mode}
        )
