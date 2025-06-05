# Author: W.K,Y.M DE SILVA
# Date: 01/11/2024
# Student ID: w2120431(Westminster)\20232969(IIT)

# Task A: Input Validation
def generate_csv_filename(date_input):
    """
    Generates a CSV file name based on the date input in the format DDMMYYYY.
    The file name format is 'traffic_dataDDMMYYYY.csv'.
    """
    return f"traffic_data{date_input}.csv"

def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format and validates the input.
    Returns the validated date and corresponding CSV file name.
    """
    day, month, year = None, None, None
    while True:
        try:
            if day is None:
                day = int(input("Please enter the day of the survey in the format DD: "))
                if not 1 <= day <= 31:
                    print("Out of range - values must be in the range 1 and 31.")
                    day = None
                    continue

            if month is None:
                month = int(input("Please enter the month of the survey in the format MM: "))
                if not 1 <= month <= 12:
                    print("Out of range - values must be in the range 1 and 12.")
                    month = None
                    continue

            if year is None:
                year = int(input("Please enter the year of the survey in the format YYYY: "))
                if not 2000 <= year <= 2024:
                    print("Out of range - values must be in the range 2000 and 2024.")
                    year = None
                    continue

            date_str = f"{day:02d}{month:02d}{year}"
            csv_file = generate_csv_filename(date_str)
            return csv_file
        except ValueError:
            print("Integer required")


# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts requested metrics.
    """
    outcomes = {
        "The total number of vehicles recorded for this date is": 0,
        "The total number of trucks recorded for this date is": 0,
        "The total number of electric vehicles for this date is": 0,
        "The total number of two—wheeled vehicles for this date is": 0,
        "The total number of Busses leaving Elm Avenue/Rabbit Road heading North is": 0,
        "The total number of Vehicles through both junctions not turning left or right is": 0,
        "The percentage of total vehicles recorded that are trucks for this date is": 0,
        "The average number of Bikes per hour for this date is": 0,
        "The total number of Vehicles recorded as over the speed limit for this date is": 0,
        "The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is": 0,
        "The total number of vehicles recorded through Hanley Highway/Westway junction is": 0,
        "of vehicles recorded through Elm Avenue/Rabbit Road that are scooters": 0,
        "The highest number of vehicles in an hour on Hanley Highway/Westway is": 0,
        "The most vehicles through Hanley Highway/Westway were recorded between": [],
        "The number of hours of rain for this date is": 0,
    }

    try:
        with open(file_path, "r") as file:
            data = file.readlines()[1:]  # Skip the header row
            if not data:
                print(f"The file '{file_path}' is empty.")
                return None
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return None

    # Helper variables for calculations
    scooter_count_elm = 0
    bicycle_count = 0
    hours = {}

    for row in data:
        fields = row.strip().split(",")
        if len(fields) != 10:  # Assuming the CSV should have 10 fields
            print(f"Skipping invalid row: {row}")
            continue

        junction, date, time, direction_in, direction_out, weather, speed_limit, vehicle_speed, vehicle_type, electric = fields

        # Increment total vehicles
        outcomes["The total number of vehicles recorded for this date is"] += 1

        # Trucks
        if vehicle_type.lower() == "truck":
            outcomes["The total number of trucks recorded for this date is"] += 1

        # Electric vehicles
        if electric.lower() == "true":
            outcomes["The total number of electric vehicles for this date is"] += 1

        # Two-wheeled vehicles
        if vehicle_type.lower() in ["bicycle", "motorcycle", "scooter"]:
            outcomes["The total number of two—wheeled vehicles for this date is"] += 1
            if vehicle_type.lower() == "bicycle":
                bicycle_count += 1

        # Buses leaving Elm Avenue/Rabbit Road heading North
        if junction == "Elm Avenue/Rabbit Road" and direction_out == "N" and vehicle_type.lower() == "buss":
            outcomes["The total number of Busses leaving Elm Avenue/Rabbit Road heading North is"] += 1

        # Straight-traveling vehicles
        if direction_in == direction_out:
            outcomes["The total number of Vehicles through both junctions not turning left or right is"] += 1

        # Vehicles over speed limit
        if int(vehicle_speed) > int(speed_limit):
            outcomes["The total number of Vehicles recorded as over the speed limit for this date is"] += 1

        # Vehicles at each junction
        if junction == "Elm Avenue/Rabbit Road":
            outcomes["The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is"] += 1
            if vehicle_type.lower() == "scooter":
                scooter_count_elm += 1
        if junction == "Hanley Highway/Westway":
            outcomes["The total number of vehicles recorded through Hanley Highway/Westway junction is"] += 1
            hour = time.split(":")[0]
            hours[hour] = hours.get(hour, 0) + 1

        # Rain hours
        if weather.lower() == "rain":
            outcomes["The number of hours of rain for this date is"] += 1

    # Calculations
    total_vehicles = outcomes["The total number of vehicles recorded for this date is"]
    if total_vehicles > 0:
        outcomes["The percentage of total vehicles recorded that are trucks for this date is"] = f"{round((outcomes['The total number of trucks recorded for this date is'] / total_vehicles) * 100)}%"

        elm_total = outcomes["The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is"]
        if elm_total > 0:
            outcomes["of vehicles recorded through Elm Avenue/Rabbit Road that are scooters"] = round(
                (scooter_count_elm / elm_total) * 100
                
            )

        outcomes["The average number of Bikes per hour for this date is"] = round(bicycle_count / 24)

    # Find highest vehicles per hour on Hanley Highway/Westway
    max_vehicles = max(hours.values(), default=0)
    outcomes["The highest number of vehicles in an hour on Hanley Highway/Westway is"] = max_vehicles
    intervals = [f"{hour}:00 and {int(hour) + 1}:00" for hour, count in hours.items() if count == max_vehicles]
    outcomes["The most vehicles through Hanley Highway/Westway were recorded between"] = " and ".join(intervals)  # Join intervals into a single string
    

    return outcomes


def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a formatted way.
    """
    print("\n***************************")
    print(f"Selected file: {csv_file}") # Added f-string for csv_file
    print("***************************")
    for key, value in outcomes.items():
        if key == "of vehicles recorded through Elm Avenue/Rabbit Road that are scooters":
            print(f"{value}% {key}")  # Special case for scooters
        else:
            print(f"{key} {value}")


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file.
    """
    with open(file_name, "a") as file:
        for key, value in outcomes.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")

# Main Program
if __name__ == "__main__":
    while True:
        csv_file = validate_date_input()
        outcomes = process_csv_data(csv_file)
        
        if outcomes:
            display_outcomes(outcomes)
            save_results_to_file(outcomes)
            break # Added break statement here to prevent infinite loop
