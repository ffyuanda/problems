def driving_cost(driven_miles, miles_per_gallon, dollars_per_gallon):
    return driven_miles / miles_per_gallon * dollars_per_gallon


miles = [10,50,400]
if __name__ == '__main__':
    # Type your code here.
    miles_per_gallon = float(input())
    dollars_per_gallon = float(input())
    for i in range(3):
        driving_cost(miles[i], miles_per_gallon, dollars_per_gallon)

