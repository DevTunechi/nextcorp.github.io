#!/usr/bin/python3
"""Handler for employee check-in and check-out operations using the API."""

from flask import flash
import requests
from datetime import datetime, timedelta


API_URL = 'http://localhost:5000/api'


def handle_checkin(employee_id):
    """
        Handles automatic employee check-in on login via API.
        Convert datetime to ISO format
        Check for any active check-ins (those without a checkout time)
        checks check-in if there's an active one
        Check for any recent check-ins (within the last minute)
        that are checked out
    """
    now = datetime.utcnow()
    checkin_data = {"checkin": now.isoformat()}

    response = requests.get(f"{API_URL}/employees/{employee_id}/checkers")

    if response.status_code == 200:
        checkers = response.json()
        active_checkin = next((c for c in checkers if c.get('checkout') is None), None)
        if active_checkin:
            print("Employee is already checked in.")
            return

        recent_checkin = next(
            (
                c
                for c in checkers
                if (now - datetime.fromisoformat(c["checkin"]))
                < timedelta(minutes=1)
            ),
            None,
        )
        if recent_checkin:
            if recent_checkin.get('checkout') is None:
                print("Employee has already checked in within the last minute.")
                return
            else:
                checkout_time = datetime.fromisoformat(recent_checkin["checkout"])
                if now - checkout_time < timedelta(minutes=1):
                    print("Employee has checked out recently, updating checkout time.")
                    payload = {'checkout': now.isoformat()}
                    response = requests.put(f"{API_URL}/checkers/{recent_checkin['id']}", json=payload)
                    if response.status_code == 200:
                        print("Checkout time updated successfully.")
                    else:
                        print(f"Error updating checkout time: {response.json()}")
                    return

    try:
        response = requests.post(
            f"{API_URL}/employees/{employee_id}/checkers", json=checkin_data
        )
        if response.status_code == 201:
            print("Employee checked in successfully.")
        else:
            print(f"Error during check-in: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error during check-in: {e}")


def handle_checkout(employee_id):
    """
        Handles automatic employee check-out on logout via API.
        Convert datetime to ISO format
        Get the latest check-in record for the employee without a checkout time
        Find the latest check-in that DOESN'T HAVE a checkout time
        Update or create a new check-in record
        Checks if There's an active check-in
    """

    now = datetime.utcnow()

    checkout_data = {'checkout': now.isoformat()}

    response = requests.get(f"{API_URL}/employees/{employee_id}/last_checkin")

    if response.status_code == 200:
        checkin_to_checkout = response.json()
    else:
        checkin_to_checkout = None

    if checkin_to_checkout:
        try:
            response = requests.put(f"{API_URL}/checkers/{checkin_to_checkout['id']}", json=checkout_data)

            if response.status_code == 200:
                print("Employee checked out successfully.")
            else:
                print(f"Error during check-out: {response.json()}")

        except requests.exceptions.RequestException as e:
            print(f"Error during check-out: {e}")

    else:
        print("No active check-in found for the employee.")

""" (Refactored)
def handle_checkout(employee_id):
        Handles automatic employee check-out on logout via API.
        Convert datetime to ISO format
        Get the latest check-in record for the employee without a checkout time
        Find the latest check-in that DOESN'T HAVE a checkout time
        Update or create a new check-in record
        Checks if There's an active check-in
    now = datetime.utcnow()
    checkout_data = {'checkout': now.isoformat()}
    response = requests.get(f"{API_URL}/employees/{employee_id}/checkers")

    print(f"[Checker Handler] GET /employees/{employee_id}/checkers response: {response.status_code}")
    print(f"[Checker Handler] Response content: {response.content}")
    
    if response.status_code == 200:
        checkers = response.json()
        print(f"[Checker Handler] Checkers data: {checkers}")

        last_checkin_to_checkout = next(
            (c for c in reversed(checkers) if c.get('checkout') is None), None
        )
    else:
        last_checkin_to_checkout = None

    if last_checkin_to_checkout:
        try:
            response = requests.put(f"{API_URL}/checkers/{last_checkin_to_checkout['id']}", json=checkout_data)
            if response.status_code == 200:
                print("Employee checked out successfully.")
            else:
                print(f"Error during check-out: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error during check-out: {e}")
    else:
        print("No active check-in found for the employee.")
"""
