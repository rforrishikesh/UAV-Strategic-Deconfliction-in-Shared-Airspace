import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_result_3d(primary, others, result):
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Primary highlighted
    px = [p[0] for p in primary["waypoints"]]
    py = [p[1] for p in primary["waypoints"]]
    pz = [p[2] for p in primary["waypoints"]]
    ax.plot(px, py, pz, linewidth=3, color="blue", label="Primary Drone")
    ax.text(px[-1], py[-1], pz[-1], "PRIMARY", color="blue")

    # Other drones
    for drone in others:
        xs = [p[0] for p in drone["waypoints"]]
        ys = [p[1] for p in drone["waypoints"]]
        zs = [p[2] for p in drone["waypoints"]]
        ax.plot(xs, ys, zs, linestyle="dashed", alpha=0.7, label=drone["id"])
        ax.text(xs[-1], ys[-1], zs[-1], drone["id"], fontsize=8)

    # Conflict highlight
    if result["conflicts"]:
        cx = []
        cy = []
        cz = []
        for drone in [primary] + others:
            for wp in drone["waypoints"]:
                cx.append(wp[0])
                cy.append(wp[1])
                cz.append(wp[2])
        ax.scatter(cx, cy, cz, s=20, color="red", label="Risk Areas")

    # Heatmap
    heatmap = result["heatmap"]
    if heatmap:
        X = [cell[0]*50 for cell in heatmap.keys()]
        Y = [cell[1]*50 for cell in heatmap.keys()]
        C = list(heatmap.values())

        scatter = ax.scatter(X, Y, [0]*len(X), c=C, cmap="jet", s=80, alpha=.6)
        fig.colorbar(scatter, label="Density Level")

    ax.set_title("3D Airspace Conflict + Density Map")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Altitude (m)")
    ax.legend(loc="upper left")

    plt.show()
