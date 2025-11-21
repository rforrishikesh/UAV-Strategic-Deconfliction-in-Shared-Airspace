"""
simulator.py
Responsible for computing drone position at any given time t
based on waypoint list and mission time window.
"""

def position_at_time(mission, t):
    waypoints = mission["waypoints"]
    t_start, t_end = mission["time_window"]

    if t < t_start:
        return None
    if t > t_end:
        return waypoints[-1]

    total_time = t_end - t_start
    num_segments = len(waypoints) - 1
    time_per_segment = total_time / num_segments

    time_since_start = t - t_start
    segment_index = int(time_since_start // time_per_segment)

    if segment_index >= num_segments:
        return waypoints[-1]

    (x1, y1, z1) = waypoints[segment_index]
    (x2, y2, z2) = waypoints[segment_index + 1]

    t0 = segment_index * time_per_segment
    fraction = (time_since_start - t0) / time_per_segment

    x = x1 + fraction * (x2 - x1)
    y = y1 + fraction * (y2 - y1)
    z = z1 + fraction * (z2 - z1)

    return (x, y, z)

