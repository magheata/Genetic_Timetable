class Course:

    def __init__(self, name: str, weekly_hours: int):
        self.name = name
        self.list_classes = {}
        self.weekly_hours = weekly_hours