class CostCalculator:

    @staticmethod
    def calculateCost(self, chromosome):
        cost = self.cost_teachers_unavailability
        cost = cost + self.cost_teacher_assigned_in_more_than_one_class
        cost = cost + self.cost_class_empty_periods
        return cost

    @staticmethod
    def cost_teachers_unavailability(self):
        return 0

    @staticmethod
    def cost_teacher_assigned_in_more_than_one_class(self):
        return 0

    @staticmethod
    def cost_class_empty_periods():
        return 0