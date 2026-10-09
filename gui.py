# gui.py
# Tkinter GUI for Observation Log (from 'tk' on whiteboard)

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    tk = None

from database import DatabaseManager
from Observation import Observation, Photometric_observation, spectroscopic_observation
import visual


class ObservationGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Observation Log")
        self.root.geometry("850x550")

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Astronomical Observation Log", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Form Frame
        form = tk.LabelFrame(self.root, text="Add Observation", padx=10, pady=10)
        form.pack(fill="x", padx=15, pady=5)

        tk.Label(form, text="Target:").grid(row=0, column=0, padx=5, pady=3, sticky="e")
        self.ent_target = tk.Entry(form, width=15)
        self.ent_target.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(form, text="Observer:").grid(row=0, column=2, padx=5, pady=3, sticky="e")
        self.ent_observer = tk.Entry(form, width=15)
        self.ent_observer.grid(row=0, column=3, padx=5, pady=3)

        tk.Label(form, text="Filter:").grid(row=1, column=0, padx=5, pady=3, sticky="e")
        self.ent_filter = tk.Entry(form, width=15)
        self.ent_filter.insert(0, "R")
        self.ent_filter.grid(row=1, column=1, padx=5, pady=3)

        tk.Label(form, text="Exposure (s):").grid(row=1, column=2, padx=5, pady=3, sticky="e")
        self.ent_exposure = tk.Entry(form, width=15)
        self.ent_exposure.grid(row=1, column=3, padx=5, pady=3)

        btn_add = tk.Button(form, text="Add", command=self.add_observation, width=10, bg="#d4edda")
        btn_add.grid(row=0, column=4, rowspan=2, padx=15, pady=3)

        # Table Frame
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        cols = ("ID", "Target", "Observer", "Filter", "Exposure", "Type", "Date")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")
        self.tree.column("ID", width=45)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=15, pady=5)

        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Show Plots", command=self.show_plots).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.load_data).pack(side="left", padx=5)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.db.get_all()
        for r in records:
            self.tree.insert("", "end", values=(r.id, r.target, r.observer, r.filter, r.exposure, r.obs_type, r.date))

    def add_observation(self):
        target = self.ent_target.get().strip()
        observer = self.ent_observer.get().strip()
        filt = self.ent_filter.get().strip()
        exp_text = self.ent_exposure.get().strip()

        if not target or not observer or not exp_text:
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        try:
            exposure = float(exp_text)
        except ValueError:
            messagebox.showerror("Error", "Exposure must be a number.")
            return

        obs = Observation(target, observer, filt, exposure)
        self.db.add_observation(obs)
        self.load_data()

        self.ent_target.delete(0, "end")
        self.ent_observer.delete(0, "end")
        self.ent_exposure.delete(0, "end")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a row to delete.")
            return

        item = self.tree.item(selected[0])
        obs_id = item["values"][0]
        if messagebox.askyesno("Confirm", f"Delete observation #{obs_id}?"):
            self.db.delete(obs_id)
            self.load_data()

    def show_plots(self):
        visual.plot_dashboard(self.db)


def launch_gui(db):
    if tk is None:
        print("Tkinter is not installed on this system.")
        return
    root = tk.Tk()
    app = ObservationGUI(root, db)
    root.mainloop()


if __name__ == "__main__":
    db = DatabaseManager()
    db.seed_data()
    launch_gui(db)
