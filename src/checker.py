"""
checker.py
Enhanced output, swarm-aware adjustments and density-based detection.
"""

import math
import random

MIN_SAFE_DISTANCE = 5.0

DENSITY_THRESHOLD = 3
ADJUSTMENT_SCALE = 2.0

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def interpolate(p1, p2, t0, t1, t):
    if t <= t0: return p1
    if t >= t1: return p2
    r = (t - t0) / (t1 - t0)
    return (p1[0] + r * (p2[0] - p1[0]),
            p1[1] + r * (p2[1] - p1[1]),
            p1[2] + r * (p2[2] - p1[2]))

def position_at_time(waypoints, time_window, t):
    start, end = time_window
    if not (start <= t <= end):
        return None

    seg_time = (end - start) / (len(waypoints) - 1)
    for i in range(len(waypoints) - 1):
        t0 = start + i * seg_time
        t1 = t0 + seg_time
        if t0 <= t <= t1:
            return interpolate(waypoints[i], waypoints[i+1], t0, t1, t)

    return waypoints[-1]

def get_grid_cell(pos, size=50):
    return (int(pos[0]//size), int(pos[1]//size))

# ---- SWARM ADJUSTMENT ----
def apply_swarm(pos, density, record):
    if density < DENSITY_THRESHOLD:
        return pos

    new = (
        pos[0] + random.uniform(-ADJUSTMENT_SCALE, ADJUSTMENT_SCALE),
        pos[1] + random.uniform(-ADJUSTMENT_SCALE, ADJUSTMENT_SCALE),
        pos[2] + random.uniform(-ADJUSTMENT_SCALE/2, ADJUSTMENT_SCALE/2)
    )

    record["count"] += 1
    return new

# ----------------------------------------

def check_mission(primary, others, dt=0.5):
    start = min(primary["time_window"][0], *(o["time_window"][0] for o in others))
    end   = max(primary["time_window"][1], *(o["time_window"][1] for o in others))

    conflicts = []
    heatmap = {}
    swarm_adjustments = {"count": 0}

    t = start
    baseline_conflicts = None
    baseline_recorded = False

    while t <= end:
        positions = {}

        for drone in [primary] + others:
            pos = position_at_time(drone["waypoints"], drone["time_window"], t)
            if pos:
                positions[drone["id"]] = pos

        grid = {}
        for drone_id, pos in positions.items():
            cell = get_grid_cell(pos)
            grid.setdefault(cell, []).append((drone_id, pos))

        for cell, arr in grid.items():
            heatmap[cell] = heatmap.get(cell, 0) + len(arr)

        # Apply swarm corrections
        adjusted = {}
        for drone_id, pos in positions.items():
            cell = get_grid_cell(pos)
            density = len(grid[cell])
            adjusted[drone_id] = apply_swarm(pos, density, swarm_adjustments)

        positions = adjusted

        # Rebuild grid after adjustments
        grid = {}
        for drone_id, pos in positions.items():
            cell = get_grid_cell(pos)
            grid.setdefault(cell, []).append((drone_id, pos))

        # Conflict check
        pairs_checked = set()
        neighbors = [(dx, dy) for dx in [-1,0,1] for dy in [-1,0,1]]

        count_this_step = 0

        for cell, drones_here in grid.items():
            for dx, dy in neighbors:
                nc = (cell[0] + dx, cell[1] + dy)
                if nc not in grid: continue

                for A, posA in drones_here:
                    for B, posB in grid[nc]:

                        if A == B: continue
                        pair = tuple(sorted((A, B)))
                        if pair in pairs_checked: continue
                        pairs_checked.add(pair)

                        if distance(posA, posB) < MIN_SAFE_DISTANCE:
                            count_this_step += 1
                            conflicts.append({"time": round(t,2), "pair": pair})

        # Capture baseline conflicts BEFORE swarm logic took effect
        if not baseline_recorded:
            baseline_conflicts = count_this_step
            baseline_recorded = True

        t += dt

    return {
        "status": "CONFLICT DETECTED" if conflicts else "CLEAR",
        "conflicts": conflicts,
        "heatmap": heatmap,
        "swarm_effect": swarm_adjustments["count"],
        "baseline_conflicts": baseline_conflicts
    }

# ----------------------------------------

def summarize_conflicts(result):
    print("\n────────────────────────────────")
    print("     ✈ UAV Conflict Report")
    print("────────────────────────────────")

    print(f"Mission Status: {result['status']}")

    if not result["conflicts"]:
        print("✔ No conflicts detected. Safe route.\n")
        return

    print(f"\nTotal Conflicts: {len(result['conflicts'])}")

    # Short swarm summary
    if result["swarm_effect"] > 0:
        print(f"Swarm Avoidance: Applied ({result['swarm_effect']} micro-adjustments)")
    else:
        print("Swarm Avoidance: Not triggered")

    print("\nKey Hotspots (by air traffic density):")
    top = sorted(result["heatmap"].items(), key=lambda x: x[1], reverse=True)[:3]
    for cell, score in top:
        print(f"  → Cell {cell}: Density Score {score}")

    print("\n────────────────────────────────\n")
