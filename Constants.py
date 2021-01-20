import enum

FILE_EXCEL_DATA = "data.xlsx"
FILE_EXCEL_RESULTS = "resultados_horarios.xls"
FILE_EXCEL_EVOLUTION = "evolucion_costes.xls"

SHEET_INFO = "info"
SHEET_TEACHER_INFO = "teacher_hours_hard"
SHEET_CLASS_TEACHERS_INFO = "class_teachers"
SHEET_COURSE_HOURS_INFO = "course_hours"

COURSES = ['1ESO', '2ESO', '3ESO', '4ESO', '1BATX', '2BATX']

DAYS_PER_WEEK = 5
WEEK_DAYS = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES']

HOURS_PER_DAY = 7
HOUR_START_DAY = 8
HOUR_END_DAY = 15

TIME_SLOTS = HOURS_PER_DAY * DAYS_PER_WEEK

MAXIMUM_GENERATIONS = 1
TOTAL_PARENTS = 10
POPULATION_SIZE = 30
DESCENDANTS = 10
MUTATION = 0.35

HCW = 1000
SCW = 5
CONSTRAINTS = ["H1", "H5", "S1", "S2", "S3", "S4", "S5"]

GRAPH_BEST_INDIVIDUAL = "BestIndPlot.jpeg"
GRAPH_GENERATION = "GenerationCostPlot.jpeg"
GRAPH_CONSTRAINT_EVOLUTION = "ConstraintsEvolution.jpeg"

DIR_GRAPH_RESULTS = "Graph_Results"


class Parent_Selection_Type(enum.Enum):
    ROULETTE = 1,
    TOURNAMENT = 2
