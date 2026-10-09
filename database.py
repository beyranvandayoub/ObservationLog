# database.py
# SQLite Database for Observation Log (Session 17 & 20)

import sqlite3
import os
from Observation import Observation, Photometric_observation, spectroscopic_observation

DB_NAME = os.path.join(os.path.dirname(__file__), "observations.db")


class DatabaseManager:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Observation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            observer TEXT,
            filter_name TEXT,
            exposure REAL,
            obs_type TEXT,
            extra_info TEXT,
            date TEXT,
            notes TEXT
        )
        """)
        conn.commit()
        conn.close()

    def add_observation(self, obs):
        conn = self.get_connection()
        cursor = conn.cursor()

        extra = ""
        if hasattr(obs, "wavelength"):
            extra = str(obs.wavelength)
        elif hasattr(obs, "resolution"):
            extra = str(obs.resolution)

        cursor.execute("""
        INSERT INTO Observation (target, observer, filter_name, exposure, obs_type, extra_info, date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (obs.target, obs.observer, obs.filter, obs.exposure, obs.obs_type, extra, obs.date, obs.notes))

        conn.commit()
        obs_id = cursor.lastrowid
        obs.id = obs_id
        conn.close()
        return obs_id

    def get_all(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, target, observer, filter_name, exposure, obs_type, extra_info, date, notes FROM Observation")
        rows = cursor.fetchall()
        conn.close()

        observations = []
        for r in rows:
            obs_id, target, observer, filt, exposure, obs_type, extra, date, notes = r
            if obs_type == "Photometric":
                try:
                    w = float(extra)
                except (ValueError, TypeError):
                    w = 0.0
                obs = Photometric_observation(target, observer, filt, exposure, w, date, notes, obs_id)
            elif obs_type == "Spectroscopic":
                obs = spectroscopic_observation(target, observer, filt, exposure, extra, date, notes, obs_id)
            else:
                obs = Observation(target, observer, filt, exposure, date, notes, obs_id)
            observations.append(obs)
        return observations

    def get_by_id(self, obs_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, target, observer, filter_name, exposure, obs_type, extra_info, date, notes FROM Observation WHERE id = ?", (obs_id,))
        r = cursor.fetchone()
        conn.close()
        if not r:
            return None

        obs_id, target, observer, filt, exposure, obs_type, extra, date, notes = r
        if obs_type == "Photometric":
            w = float(extra) if extra else 0.0
            return Photometric_observation(target, observer, filt, exposure, w, date, notes, obs_id)
        elif obs_type == "Spectroscopic":
            return spectroscopic_observation(target, observer, filt, exposure, extra, date, notes, obs_id)
        else:
            return Observation(target, observer, filt, exposure, date, notes, obs_id)

    def search(self, target=None, observer=None, filter_name=None):
        conn = self.get_connection()
        cursor = conn.cursor()

        query = "SELECT id, target, observer, filter_name, exposure, obs_type, extra_info, date, notes FROM Observation WHERE 1=1"
        params = []

        if target:
            query += " AND LOWER(target) LIKE ?"
            params.append(f"%{target.lower()}%")
        if observer:
            query += " AND LOWER(observer) LIKE ?"
            params.append(f"%{observer.lower()}%")
        if filter_name:
            query += " AND LOWER(filter_name) = ?"
            params.append(filter_name.lower())

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        results = []
        for r in rows:
            obs_id, t, obs, f, exp, otype, extra, date, notes = r
            if otype == "Photometric":
                w = float(extra) if extra else 0.0
                item = Photometric_observation(t, obs, f, exp, w, date, notes, obs_id)
            elif otype == "Spectroscopic":
                item = spectroscopic_observation(t, obs, f, exp, extra, date, notes, obs_id)
            else:
                item = Observation(t, obs, f, exp, date, notes, obs_id)
            results.append(item)
        return results

    def update(self, obs_id, target=None, observer=None, filter_name=None, exposure=None, notes=None):
        conn = self.get_connection()
        cursor = conn.cursor()

        fields = []
        params = []
        if target:
            fields.append("target = ?")
            params.append(target)
        if observer:
            fields.append("observer = ?")
            params.append(observer)
        if filter_name:
            fields.append("filter_name = ?")
            params.append(filter_name)
        if exposure is not None:
            fields.append("exposure = ?")
            params.append(float(exposure))
        if notes is not None:
            fields.append("notes = ?")
            params.append(notes)

        if not fields:
            conn.close()
            return False

        params.append(obs_id)
        query = f"UPDATE Observation SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        return changed

    def delete(self, obs_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Observation WHERE id = ?", (obs_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    def get_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            COUNT(*),
            SUM(exposure),
            AVG(exposure),
            MIN(exposure),
            MAX(exposure),
            COUNT(DISTINCT target),
            COUNT(DISTINCT observer)
        FROM Observation
        """)
        row = cursor.fetchone()
        conn.close()

        count, total_exp, avg_exp, min_exp, max_exp, n_targets, n_observers = row
        return {
            "count": count or 0,
            "total_exp": total_exp or 0.0,
            "avg_exp": round(avg_exp, 2) if avg_exp else 0.0,
            "min_exp": min_exp or 0.0,
            "max_exp": max_exp or 0.0,
            "targets": n_targets or 0,
            "observers": n_observers or 0
        }

    def to_dataframe(self):
        # Reading SQL query with pandas (Session 20)
        try:
            import pandas as pd
            conn = self.get_connection()
            df = pd.read_sql_query("SELECT * FROM Observation", conn)
            conn.close()
            return df
        except ImportError:
            return None

    def seed_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Observation")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return 0
        conn.close()

        samples = [
            Observation("M31", "Dornika", "R", 180, "2024-10-01 21:15", "Andromeda Galaxy"),
            Observation("M45", "Hasti", "G", 220, "2024-10-01 22:30", "Pleiades cluster"),
            Observation("M33", "Anisa", "i", 600, "2024-10-02 01:10", "Triangulum Galaxy"),
            Photometric_observation("Moon", "Elham", "z", 20, 900.0, "2024-10-03 20:00", "Tycho crater"),
            Observation("M10", "Navid", "B", 280, "2024-10-04 23:45", "Globular cluster"),
            Observation("M31", "Romina", "i", 280, "2024-10-05 22:15", "Andromeda disk"),
            Observation("M45", "Mahdieh", "V", 120, "2024-10-06 20:30", "Pleiades stars"),
            spectroscopic_observation("Vega", "Dornika", "Clear", 45, "High", "2024-10-07 19:50", "Balmer lines")
        ]
        for s in samples:
            self.add_observation(s)
        return len(samples)

    # Aliases
    get_all_observations = get_all
    get_observation_by_id = get_by_id
    search_observations = search
    delete_observation = delete
    update_observation = update
    get_statistics = get_stats
    seed_sample_data = seed_data
