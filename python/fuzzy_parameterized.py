import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ============================================================
# PARAMETERIZED FUZZY CONTROLLER
# ============================================================

def create_fuzzy_controller(parameters):

    # --------------------------------------------------------
    # Read parameters
    # --------------------------------------------------------

    q_low_center = parameters[0]
    q_low_sigma = parameters[1]

    q_medium_center = parameters[2]
    q_medium_sigma = parameters[3]

    q_high_center = parameters[4]
    q_high_sigma = parameters[5]

    a_low_center = parameters[6]
    a_low_sigma = parameters[7]

    a_medium_center = parameters[8]
    a_medium_sigma = parameters[9]

    a_high_center = parameters[10]
    a_high_sigma = parameters[11]


    # --------------------------------------------------------
    # Variables
    # --------------------------------------------------------

    queue = ctrl.Antecedent(
        np.arange(0, 31, 1),
        'queue'
    )

    arrival = ctrl.Antecedent(
        np.arange(0, 11, 1),
        'arrival'
    )

    green_change = ctrl.Consequent(
        np.arange(-10, 11, 1),
        'green_change'
    )


    # --------------------------------------------------------
    # Queue membership functions
    # --------------------------------------------------------

    queue['low'] = fuzz.gaussmf(
        queue.universe,
        q_low_center,
        q_low_sigma
    )

    queue['medium'] = fuzz.gaussmf(
        queue.universe,
        q_medium_center,
        q_medium_sigma
    )

    queue['high'] = fuzz.gaussmf(
        queue.universe,
        q_high_center,
        q_high_sigma
    )


    # --------------------------------------------------------
    # Arrival membership functions
    # --------------------------------------------------------

    arrival['low'] = fuzz.gaussmf(
        arrival.universe,
        a_low_center,
        a_low_sigma
    )

    arrival['medium'] = fuzz.gaussmf(
        arrival.universe,
        a_medium_center,
        a_medium_sigma
    )

    arrival['high'] = fuzz.gaussmf(
        arrival.universe,
        a_high_center,
        a_high_sigma
    )


    # --------------------------------------------------------
    # Output membership functions
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Nine rules
    # --------------------------------------------------------

    rules = [

        ctrl.Rule(
            queue['low'] & arrival['low'],
            green_change['shorten']
        ),

        ctrl.Rule(
            queue['low'] & arrival['medium'],
            green_change['no_change']
        ),

        ctrl.Rule(
            queue['low'] & arrival['high'],
            green_change['extend']
        ),

        ctrl.Rule(
            queue['medium'] & arrival['low'],
            green_change['no_change']
        ),

        ctrl.Rule(
            queue['medium'] & arrival['medium'],
            green_change['extend']
        ),

        ctrl.Rule(
            queue['medium'] & arrival['high'],
            green_change['extend_greatly']
        ),

        ctrl.Rule(
            queue['high'] & arrival['low'],
            green_change['extend']
        ),

        ctrl.Rule(
            queue['high'] & arrival['medium'],
            green_change['extend_greatly']
        ),

        ctrl.Rule(
            queue['high'] & arrival['high'],
            green_change['extend_greatly']
        )
    ]


    # --------------------------------------------------------
    # Create controller
    # --------------------------------------------------------

    system = ctrl.ControlSystem(rules)

    simulation = ctrl.ControlSystemSimulation(system)

    return simulation


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # These are our current hand-selected parameters.
    test_parameters = [

        # Queue
        0, 5,
        15, 5,
        30, 5,

        # Arrival
        0, 2,
        5, 2,
        10, 2
    ]

    controller = create_fuzzy_controller(
        test_parameters
    )

    controller.input['queue'] = 20
    controller.input['arrival'] = 8

    controller.compute()

    result = controller.output['green_change']

    print(
        "Green-time adjustment:",
        round(result, 2),
        "seconds"
    )