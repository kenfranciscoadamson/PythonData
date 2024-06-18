import math

def get_actual_cost(sqft_walls, sqft_ceiling, sqft_per_gallon, cost_per_gallon):
    cost = cost_per_gallon * math.ceil((sqft_walls + sqft_ceiling) / sqft_per_gallon)
    return cost

actual_cost1 = get_actual_cost(432, 144, 400, 15)
print(actual_cost1)

actual_cost2 = get_actual_cost(594, 288, 400, 15) 
print(actual_cost2)