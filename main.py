# main.py
# Astronomy Observation Log - Main Program

import csv
from Observation import Observation, Photometric_observation, spectroscopic_observation
from database import DatabaseManager
import visual


def show_table(observations):
    if not observations:
        print("\nNo observations found.\n")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<4} {'Target':<10} {'Observer':<10} {'Filter':<8} {'Exp(s)':<8} {'Type':<14} {'Date'}")
    print("-" * 75)
    for obs in observations:
        print(f"{obs.id:<4} {obs.target:<10} {obs.observer:<10} {obs.filter:<8} {obs.exposure:<8.1f} {obs.obs_type:<14} {obs.date}")
    print("-" * 75 + "\n")


def add_observation_menu(db):
    print("\n--- Add Observation ---")
    target = input("Target (e.g. M31, M45): ").strip()
    if not target:
        print("Target cannot be empty.")
        return

    observer = input("Observer name: ").strip()
    if not observer:
        print("Observer name cannot be empty.")
        return

    filt = input("Filter (R, G, B, V, i, z, Clear) [Default: R]: ").strip() or "R"

    try:
        exposure = float(input("Exposure time (seconds): ").strip())
        if exposure <= 0:
            print("Exposure time must be positive.")
            return
    except ValueError:
        print("Please enter a valid number for exposure.")
        return

    print("Type: 1) General  2) Photometric  3) Spectroscopic")
    t_choice = input("Select type (1-3) [1]: ").strip() or "1"
    notes = input("Notes (optional): ").strip()

    if t_choice == "2":
        try:
            w = float(input("Wavelength (nm): ").strip())
        except ValueError:
            w = 550.0
        obs = Photometric_observation(target, observer, filt, exposure, w, notes=notes)
    elif t_choice == "3":
        res = input("Resolution [Medium]: ").strip() or "Medium"
        obs = spectroscopic_observation(target, observer, filt, exposure, res, notes=notes)
    else:
        obs = Observation(target, observer, filt, exposure, notes=notes)

    new_id = db.add_observation(obs)
    print(f"Observation added successfully with ID {new_id}!")


def search_observation_menu(db):
    print("\n--- Search Observation ---")
    print("1. Search by Target")
    print("2. Search by Observer")
    choice = input("Choice (1-2): ").strip()

    if choice == "1":
        query = input("Target name: ").strip()
        results = db.search(target=query)
    elif choice == "2":
        query = input("Observer name: ").strip()
        results = db.search(observer=query)
    else:
        print("Invalid choice.")
        return

    show_table(results)


def delete_observation_menu(db):
    print("\n--- Delete Observation ---")
    try:
        obs_id = int(input("Enter ID to delete: ").strip())
        obs = db.get_by_id(obs_id)
        if not obs:
            print(f"Observation #{obs_id} not found.")
            return

        confirm = input(f"Are you sure you want to delete {obs.target} (#{obs_id})? (y/n): ").strip().lower()
        if confirm == "y":
            if db.delete(obs_id):
                print(f"Observation #{obs_id} deleted successfully.")
            else:
                print("Failed to delete.")
    except ValueError:
        print("Invalid ID.")


def update_observation_menu(db):
    print("\n--- Update Observation ---")
    try:
        obs_id = int(input("Enter ID to update: ").strip())
        obs = db.get_by_id(obs_id)
        if not obs:
            print(f"Observation #{obs_id} not found.")
            return

        print(f"Current values: Target={obs.target}, Observer={obs.observer}, Filter={obs.filter}, Exposure={obs.exposure}")
        print("(Press enter to keep current value)")

        target = input(f"New Target [{obs.target}]: ").strip() or None
        observer = input(f"New Observer [{obs.observer}]: ").strip() or None
        filt = input(f"New Filter [{obs.filter}]: ").strip() or None
        exp_in = input(f"New Exposure [{obs.exposure}]: ").strip()
        exp = float(exp_in) if exp_in else None
        notes = input(f"New Notes [{obs.notes}]: ").strip() or None

        if db.update(obs_id, target, observer, filt, exp, notes):
            print(f"Observation #{obs_id} updated successfully.")
        else:
            print("No changes made.")
    except ValueError:
        print("Invalid input.")


def show_statistics(db):
    stats = db.get_stats()
    print("\n" + "=" * 35)
    print("      Observation Statistics")
    print("=" * 35)
    print(f"Total observations : {stats['count']}")
    print(f"Total exposure time: {stats['total_exp']:.1f} s ({stats['total_exp']/60:.2f} min)")
    print(f"Average exposure   : {stats['avg_exp']:.1f} s")
    print(f"Min exposure       : {stats['min_exp']:.1f} s")
    print(f"Max exposure       : {stats['max_exp']:.1f} s")
    print(f"Unique targets     : {stats['targets']}")
    print(f"Unique observers   : {stats['observers']}")
    print("=" * 35)

    # Pandas groupby summary (Session 20)
    df = db.to_dataframe()
    if df is not None and not df.empty:
        print("\nTarget Summary (Pandas GroupBy):")
        summary = df.groupby("target")["exposure"].agg(["count", "sum", "mean"]).round(1)
        summary.columns = ["Count", "Total(s)", "Mean(s)"]
        print(summary)


def visual_menu(db):
    while True:
        print("\n--- Visualization Menu ---")
        print("1. Exposure by Target (Bar chart)")
        print("2. Filter Distribution (Pie chart)")
        print("3. Observer Exposure (Bar chart)")
        print("4. Complete 4-Panel Dashboard")
        print("0. Back")

        choice = input("Choice: ").strip()
        if choice == "1":
            visual.plot_exposure_by_target(db)
        elif choice == "2":
            visual.plot_filter_distribution(db)
        elif choice == "3":
            visual.plot_observer_contributions(db)
        elif choice == "4":
            visual.plot_dashboard(db)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def export_csv(db):
    filename = input("Filename [observations.csv]: ").strip() or "observations.csv"
    if not filename.endswith(".csv"):
        filename += ".csv"

    records = db.get_all()
    if not records:
        print("No observations to export.")
        return

    keys = ["id", "target", "observer", "filter", "exposure", "exposure_min", "obs_type", "wavelength", "resolution", "date", "notes"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            writer.writerow(r.to_dict())
    print(f"Exported {len(records)} observations to {filename}")


def run_gui(db):
    try:
        from gui import launch_gui
        launch_gui(db)
    except Exception as e:
        print("Could not open GUI:", e)


def main():
    db = DatabaseManager()
    db.seed_data()

    while True:
        print("\n" + "=" * 40)
        print("       Observation Log System")
        print("=" * 40)
        print("1. Add Observation")
        print("2. Show Observations")
        print("3. Search Observation")
        print("4. Update Observation")
        print("5. Delete Observation")
        print("6. Statistics")
        print("7. Visualizations")
        print("8. Export to CSV")
        print("9. Launch GUI (Tkinter)")
        print("0. Exit")
        print("=" * 40)

        choice = input("Select an option (0-9): ").strip()

        if choice == "1":
            add_observation_menu(db)
        elif choice == "2":
            show_table(db.get_all())
        elif choice == "3":
            search_observation_menu(db)
        elif choice == "4":
            update_observation_menu(db)
        elif choice == "5":
            delete_observation_menu(db)
        elif choice == "6":
            show_statistics(db)
        elif choice == "7":
            visual_menu(db)
        elif choice == "8":
            export_csv(db)
        elif choice == "9":
            run_gui(db)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Please enter a number between 0 and 9.")


if __name__ == "__main__":
    main()
