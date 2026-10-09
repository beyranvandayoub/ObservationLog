# Observation.py
# Astronomy Observation Log - Classes

import time

class Observation:
    def __init__(self, target, observer, filter_name, exposure, date=None, notes="", obs_id=None):
        self.target = target
        self.observer = observer
        self.filter = filter_name
        self.exposure = float(exposure)
        self.date = date if date else time.strftime("%Y-%m-%d %H:%M")
        self.notes = notes
        self.obs_type = "General"
        self.id = obs_id

    def exposure_min(self):
        return self.exposure / 60

    def summary_info(self):
        info = (
            f"Target: {self.target}\n"
            f"Observer: {self.observer}\n"
            f"Filter: {self.filter}\n"
            f"Exposure: {self.exposure} sec ({self.exposure_min():.2f} min)\n"
            f"Type: {self.obs_type}\n"
            f"Date: {self.date}"
        )
        if self.notes:
            info += f"\nNotes: {self.notes}"
        return info

    def to_dict(self):
        return {
            "id": self.id,
            "target": self.target,
            "observer": self.observer,
            "filter": self.filter,
            "exposure": self.exposure,
            "exposure_min": round(self.exposure_min(), 2),
            "obs_type": self.obs_type,
            "wavelength": getattr(self, "wavelength", ""),
            "resolution": getattr(self, "resolution", ""),
            "date": self.date,
            "notes": self.notes
        }


class Photometric_observation(Observation):
    def __init__(self, target, observer, filter_name, exposure, wavelength, date=None, notes="", obs_id=None):
        super().__init__(target, observer, filter_name, exposure, date, notes, obs_id)
        self.wavelength = float(wavelength)
        self.obs_type = "Photometric"

    def summary_info(self):
        return super().summary_info() + f"\nWavelength: {self.wavelength} nm"


class spectroscopic_observation(Observation):
    def __init__(self, target, observer, filter_name, exposure, resolution="Medium", date=None, notes="", obs_id=None):
        super().__init__(target, observer, filter_name, exposure, date, notes, obs_id)
        self.resolution = resolution
        self.obs_type = "Spectroscopic"

    def summary_info(self):
        return super().summary_info() + f"\nResolution: {self.resolution}"


# Aliases for compatibility
PhotometricObservation = Photometric_observation
SpectroscopicObservation = spectroscopic_observation
