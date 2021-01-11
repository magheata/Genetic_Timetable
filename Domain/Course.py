class Course:

    def __init__(self, name, weekly_hours):
        self.name = name
        self.list_classes = []
        self.weekly_hours = weekly_hours

    def __repr__(self):
        return f"Name: {self.name}\n" \
               f"Classes: {self.list_classes}\n" \
               f"Hours/Week: {self.weekly_hours}\n"
