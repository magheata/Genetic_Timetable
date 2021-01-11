class Class:
    def __init__(self, class_name, list_teachers):
        self.class_name = class_name
        self.list_teachers = list_teachers
        self.course = []
        self.hours_per_week = None

    def __repr__(self):
        return f"Class: {self.class_name}\n" \
               f"   Teachers: {self.list_teachers}\n" \
               f"   Course: {self.course}\n" \
               f"   Hours/Week: {self.hours_per_week}\n"

    def set_class_course(self, course):
        self.course.append(course)

    def set_hours_per_week(self, hours_per_week):
        self.hours_per_week = hours_per_week


class Lesson:
    def __init__(self, assigned_teacher, class_, time_slot):
        self.assigned_teacher = assigned_teacher
        self.class_ = class_
        self.time_slot = time_slot
