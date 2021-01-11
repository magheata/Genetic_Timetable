import numpy as np


class Teacher:
    def __init__(self, name, availability, hours_per_week):
        self.name = name
        self.aux_availability = availability
        self.availability = np.zeros(self.aux_availability['class_days'] *
                                     self.aux_availability['hours_per_day'])
        availability_idx = 0
        for availability_class_day in self.aux_availability['weekdays']:
            for i in range(0, self.aux_availability['hours_per_day']):
                self.availability[availability_idx] = self.aux_availability['weekdays'][availability_class_day]
                availability_idx = availability_idx + 1
        self.hours_per_week = hours_per_week

    def __repr__(self):
        return f"\n         Name: {self.name}\n" \
               f"           Availability: {self.availability}\n" \
               f"           Hours per week: {self.hours_per_week}\n"
