import Constants


class TimeTable:

    def __init__(self, chromosome, course):
        self.chromosome = chromosome
        self.course = course

    def __repr__(self):
        res = ""
        for column in self.chromosome:
            lesson = self.chromosome[column].array[0]
            if lesson != 0:
                class_ = lesson.class_
                teacher = lesson.assigned_teacher
                day = lesson.get_weekday()
                hour = lesson.get_hour()
                res = res + f"{day} {hour} {class_} with {teacher}\n"
        return res
