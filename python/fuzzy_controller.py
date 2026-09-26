import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ============================================================
# 1. INPUTS
# ============================================================

# Queue Length: 0–30 vehicles
queue = ctrl.Antecedent(
    np.arange(0, 31, 1),
    'queue'
)

# Arrival Rate: 0–10 vehicles per sampling interval
arrival = ctrl.Antecedent(
    np.arange(0, 11, 1),
    'arrival'
)


# ============================================================
# 2. OUTPUT
# ============================================================

# Green-time adjustment: -10 to +10 seconds
green_change = ctrl.Consequent(
    np.arange(-10, 11, 1),
    'green_change'
)


# ============================================================
# 3. GAUSSIAN MEMBERSHIP FUNCTIONS
# ============================================================

# Queue Length
queue['low'] = fuzz.gaussmf(
    queue.universe,
    0,
    5
)

queue['medium'] = fuzz.gaussmf(
    queue.universe,
    15,
    5
)

queue['high'] = fuzz.gaussmf(
    queue.universe,
    30,
    5
)


# Arrival Rate
arrival['low'] = fuzz.gaussmf(
    arrival.universe,
    0,
    2
)

arrival['medium'] = fuzz.gaussmf(
    arrival.universe,
    5,
    2
)

arrival['high'] = fuzz.gaussmf(
    arrival.universe,
    10,
    2
)


# ============================================================
# 4. FIVE GREEN-TIME OUTPUT TERMS
# ============================================================

green_change['shorten_greatly'] = fuzz.trapmf(
    green_change.universe,
    [-10, -10, -8, -5]
)

green_change['shorten'] = fuzz.trimf(
    green_change.universe,
    [-7, -4, 0]
)

green_change['no_change'] = fuzz.trimf(
    green_change.universe,
    [-2, 0, 2]
)

green_change['extend'] = fuzz.trimf(
    green_change.universe,
    [0, 4, 7]
)

green_change['extend_greatly'] = fuzz.trapmf(
    green_change.universe,
    [5, 8, 10, 10]
)


# ============================================================
# 5. NINE CORE RULES
# ============================================================

rule1 = ctrl.Rule(
    queue['low'] & arrival['low'],
    green_change['shorten']
)

rule2 = ctrl.Rule(
    queue['low'] & arrival['medium'],
    green_change['no_change']
)

rule3 = ctrl.Rule(
    queue['low'] & arrival['high'],
    green_change['extend']
)

rule4 = ctrl.Rule(
    queue['medium'] & arrival['low'],
    green_change['no_change']
)

rule5 = ctrl.Rule(
    queue['medium'] & arrival['medium'],
    green_change['extend']
)

rule6 = ctrl.Rule(
    queue['medium'] & arrival['high'],
    green_change['extend_greatly']
)

rule7 = ctrl.Rule(
    queue['high'] & arrival['low'],
    green_change['extend']
)

rule8 = ctrl.Rule(
    queue['high'] & arrival['medium'],
    green_change['extend_greatly']
)

rule9 = ctrl.Rule(
    queue['high'] & arrival['high'],
    green_change['extend_greatly']
)


# ============================================================
# 6. MAMDANI CONTROLLER
# ============================================================

fuzzy_system = ctrl.ControlSystem([
    rule1,
    rule2,
    rule3,
    rule4,
    rule5,
    rule6,
    rule7,
    rule8,
    rule9
])

fuzzy_controller = ctrl.ControlSystemSimulation(
    fuzzy_system
)


# ============================================================
# 7. FUNCTION USED BY SUMO
# ============================================================

def get_green_change(queue_length, arrival_rate):

    fuzzy_controller.input['queue'] = queue_length
    fuzzy_controller.input['arrival'] = arrival_rate

    fuzzy_controller.compute()

    return fuzzy_controller.output['green_change']


# ============================================================
# 8. TEST
# ============================================================

if __name__ == "__main__":

    queue_length = 20
    arrival_rate = 8

    result = get_green_change(
        queue_length,
        arrival_rate
    )

    print("Queue Length:", queue_length)
    print("Arrival Rate:", arrival_rate)
    print(
        "Green-time adjustment:",
        round(result, 2),
        "seconds"
    )