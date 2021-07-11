import random

AREA_SQUARE_MILES = 1.64
SCALE = 10  # each point represents a [scale] foot by [scale] foot area
MEDIAN_HOUSEHOLD_INCOME = 102486
NODE_MAX_MBPS_OUTPUT = 925
POPULATION_PER_SUBREGION = 1468, 1624, 1012, 1295, 1309, 1008, 1789
DEMAND_PER_PERSON_PER_SUBREGION_MBPS = (
    0.764702,
    0.559286,
    0.764702,
    0.764702,
    0.559286,
    0.764702,
    0.764702,
)
TRIALS = 100000
TOTAL_NODES = 5000


side = int(AREA_SQUARE_MILES ** 0.5 * 5280 / SCALE)


"""
each point in "space" has three attributes: 
	space[x][y][0] representing the RECEPTION which will be incremented depending on the proximity to a node, 
	space[x][y][1] representing the DEMAND PER UNIT AREA which will depend on which subregion the point is in, and
	space[x][y][2] representing whether whether the subregion is classified as URBAN (True) or RURAL (False) as determined in the paper
"""

space = []
for x in range(side):
    column = []
    for y in range(side):
        receptions = []
        receptions.append(0)
        receptions.append(0)
        receptions.append(True)
        column.append(receptions)
    space.append(column)

# This part of our code assigns the "subregions" and urban/rural value to our space array. We understand this is messy, but a more concise and accurate assignment would require detailed information about how each of the subregions are shaped, such as a graph with points representing a "connect the dots" for a subregion's border. This data does exist for real-world regions, however.

# assigning demand and rural/urban variables
for x in range(int(side * 0.2) + 1):
    for y in range(int(side * 0.75)):
        space[x][y][1] = (
            (POPULATION_PER_SUBREGION[0] / AREA_SQUARE_MILES)
            * (DEMAND_PER_PERSON_PER_SUBREGION_MBPS[0])
            * (1 / 5280.0) ** 2
            * (SCALE) ** 2
        )
        space[x][y][2] = False
for x in range(int(side * 0.25)):
    for y in range(int(side * 0.75 + 1), side):
        space[x][y][1] = (
            (POPULATION_PER_SUBREGION[1] / AREA_SQUARE_MILES)
            * (DEMAND_PER_PERSON_PER_SUBREGION_MBPS[1])
            * (1 / 5280.0) ** 2
            * (SCALE) ** 2
        )
for x in range(int(side * 0.25 + 1), int(side * 0.475)):
    for y in range(int(side * 0.60 + 1), side):
        space[x][y][1] = (
            (POPULATION_PER_SUBREGION[2] / AREA_SQUARE_MILES)
            * (DEMAND_PER_PERSON_PER_SUBREGION_MBPS[2])
            * (1 / 5280.0) ** 2
            * (SCALE) ** 2
        )
for x in range(int(side * 0.475 + 1), int(side * 0.7)):
    for y in range(int(side * 0.6 + 1), side):
        space[x][y][1] = (
            (POPULATION_PER_SUBREGION[3] / AREA_SQUARE_MILES)
            * (DEMAND_PER_PERSON_PER_SUBREGION_MBPS[3])
            * (1 / 5280.0) ** 2
            * (SCALE) ** 2
        )
        space[x][y][2] = False
for x in range(int(side * 0.7 + 1), side):
    for y in range(int(side * 0.4 + 1), side):
        space[x][y][1] = (
            (POPULATION_PER_SUBREGION[4] / AREA_SQUARE_MILES)
            * (DEMAND_PER_PERSON_PER_SUBREGION_MBPS[4])
            * (1 / 5280.0) ** 2
            * (SCALE) ** 2
        )
for x in range(int(side * 0.2 + 1), int(side * 0.6 + 1)):
    for y in range(int(side * 0.6 + 1)):
        space[x][y][1] = (
            (POPULATION_PER_SUBREGION[5] / AREA_SQUARE_MILES)
            * (DEMAND_PER_PERSON_PER_SUBREGION_MBPS[5])
            * (1 / 5280.0) ** 2
            * (SCALE) ** 2
        )
        space[x][y][2] = False
for x in range(int(side * 0.60 + 1), side):
    for y in range(int(side * 0.6)):
        space[x][y][1] = (
            (POPULATION_PER_SUBREGION[6] / AREA_SQUARE_MILES)
            * (DEMAND_PER_PERSON_PER_SUBREGION_MBPS[6])
            * (1 / 5280.0) ** 2
            * (SCALE) ** 2
        )
        space[x][y][2] = False


def calculate_reception(x_house, y_house, x_node, y_node, isUrban):
    global NODE_MAX_MBPS_OUTPUT, SCALE

    if isUrban:
        NODE_MAX_RANGE_FEET = 1500
    else:
        NODE_MAX_RANGE_FEET = 6547  # 1.24 miles

    NODE_MAX_RANGE = NODE_MAX_RANGE_FEET / SCALE

    distance = (
        (x_house - x_node) ** 2 + (y_house - y_node) ** 2
    ) ** 0.5  # Calculate distance between a point and the node that was just placed
    if distance < NODE_MAX_RANGE:  # If the house is within range of the tower
        return (
            925 - (NODE_MAX_MBPS_OUTPUT / NODE_MAX_RANGE) * distance
        )  # Return a reception as a function of distance, assuming that as you move further away from a node your reception decreases linearly such that once you're at the max range your reception is 0
    else:
        return 0


max_percent_houses_with_demand_met = 0.0  # value we want to maximize

best_nodes = []

for trial in range(TRIALS):

    nodes = []

    for node in range(TOTAL_NODES):
        # "Throw a dart" and that's where a node is
        x_node = random.randint(0, side)
        y_node = random.randint(0, side)
        trial_node = [x_node, y_node]

        nodes.append(trial_node)

        # Iterate over all points in space and calculate how much reception each point gets from the node that was just found
        for y_house in range(side):
            for x_house in range(side):
                space[x][y][0] += calculate_reception(
                    x_house, y_house, x_node, y_node, space[x][y][2]
                )

    this_trials_points_with_demand_met = 0
    for y_house in range(side):
        for x_house in range(side):
            if space[x_house][y_house][0] > space[x_house][y_house][1]:
                this_trials_points_with_demand_met += 1

    this_trials_percent_houses_with_demand_met = (
        this_trials_points_with_demand_met / side ** 2
    ) * 100
    if this_trials_percent_houses_with_demand_met > max_percent_houses_with_demand_met:
        max_percent_houses_with_demand_met = this_trials_percent_houses_with_demand_met
        best_nodes = nodes


print(max_percent_houses_with_demand_met)
print(best_nodes)

print("completed")
