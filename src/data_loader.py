"""
data_loader.py
Mission loading and scenario selection.
"""

import random


# -------- RANDOM GENERATION -------- #

def generate_random_drone(id, waypoint_count=3):
    """Generate a random drone mission for testing scalability."""
    waypoints = [
        (
            random.randint(0, 60),
            random.randint(-20, 60),
            random.randint(10, 80)
        )
        for _ in range(waypoint_count)
    ]

    start = random.randint(0, 20)
    end = start + random.randint(20, 60)

    return {
        "id": f"Drone_{id}",
        "waypoints": waypoints,
        "time_window": (start, end)
    }


# -------- FINAL HARDCODED MIXED SCENARIO -------- #

def load_hardcoded_mixed():
    """
    Hardcoded scenario with a mix:
    - Some drones will conflict
    - Some are safe due to altitude
    - Some never overlap in time
    """

    primary = {
        "id": "Primary",
        "waypoints": [(0, 0, 20), (30, 15, 22), (60, 35, 25)],
        "time_window": (0, 50)
    }

    others = [

        # 1️⃣ Will conflict (close path + same altitude/time)
        {
            "id": "Drone_A",
            "waypoints": [(5, 5, 22), (30, 15, 22), (60, 40, 24)],
            "time_window": (0, 50)
        },

        # 2️⃣ Safe because altitude is higher
        {
            "id": "Drone_B",
            "waypoints": [(0, 0, 60), (30, 15, 60), (60, 35, 60)],
            "time_window": (0, 50)
        },

        # 3️⃣ Safe because time window does NOT overlap
        {
            "id": "Drone_C",
            "waypoints": [(0, 0, 20), (25, 10, 22), (55, 30, 25)],
            "time_window": (60, 100)
        },

        # 4️⃣ Another conflict case, different shape
        {
            "id": "Drone_D",
            "waypoints": [(10, -5, 21), (35, 10, 22), (65, 30, 23)],
            "time_window": (5, 45)
        },

        # 5️⃣ Close but safe — near misses only
        {
            "id": "Drone_E",
            "waypoints": [(15, 10, 30), (40, 25, 32), (70, 45, 34)],
            "time_window": (0, 50)
        }
    ]

    return primary, others


# -------- RANDOM AND STRESS MODES -------- #

def load_random_missions(count=5):
    primary = {
        "id": "Primary",
        "waypoints": [(0, 0, 20), (20, 10, 25), (50, 30, 30)],
        "time_window": (0, 50)
    }

    others = [generate_random_drone(i) for i in range(1, count + 1)]
    return primary, others
