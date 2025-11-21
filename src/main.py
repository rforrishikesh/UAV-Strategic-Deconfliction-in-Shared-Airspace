from data_loader import load_hardcoded_mixed, load_random_missions
from checker import check_mission, summarize_conflicts
from visualization import plot_result_3d



def main():
    print("\n=== UAV Mission Deconfliction System ===\n")
    print("Select simulation mode:")
    print("1. Hardcoded mixed scenario (recommended)")
    print("2. Random simulation (5 drones)")
    print("3. Stress test (15 drones - no visualization)\n")

    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        primary, others = load_hardcoded_mixed()
        visualize = True

    elif choice == "2":
        primary, others = load_random_missions(8)
        visualize = True

    elif choice == "3":
        primary, others = load_random_missions(15)
        visualize = False

    else:
        print("\nInvalid option — defaulting to mixed scenario.\n")
        primary, others = load_hardcoded_mixed()
        visualize = True

    # Run system
    result = check_mission(primary, others)
    summarize_conflicts(result)

   

    # VISUALIZATIONS
    plot_result_3d(primary, others, result)
    




if __name__ == "__main__":
    main()
