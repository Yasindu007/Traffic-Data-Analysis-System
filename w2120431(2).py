# Author: W.K,Y.M DE SILVA
# Date: 24/12/2024
# Student ID: w2120431(Westminster)\20232969(IIT)
# Task D: Histogram Display
import tkinter as tk
from tkinter import Canvas
import csv

#Task D
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        - traffic_data: List of traffic records containing vehicle data.
        - date: The date of the traffic survey.
        """
        self.traffic_data = traffic_data  # Store the traffic data
        self.date = date  # Store the selected date
        self.root = tk.Tk()  # Create the main window for the application
        self.canvas = None  # Will hold the canvas for drawing the histogram

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for drawing the histogram.
        The window will display the title and contain a canvas to draw on.
        """
        self.root.title(f"Histogram of Vehicle Frequency per Hour ({self.date[:2]}/{self.date[2:4]}/{self.date[4:]})")  # Set the window title
        # Create a canvas widget where the histogram will be drawn
        self.canvas = Canvas(self.root, width=1000, height=600, bg="#E9F4E9")
        self.canvas.pack()  # Add the canvas to the window

    def aggregate_data(self):
        """
        Aggregates the traffic data by hour and junction.
        This function loops through the traffic data, extracts the hour from the 
        'timeOfDay' field, and counts how many vehicles passed each junction in 
        that hour. It returns a dictionary with hourly vehicle counts for each junction.
        
        Returns:
            dict: A dictionary with hourly vehicle counts for each junction.
        """
        # Initialize a dictionary to store the counts of vehicles per hour for each junction
        hourly_data = {hour: {"Elm Avenue/Rabbit Road": 0, "Hanley Highway/Westway": 0} for hour in range(24)}

        # Loop through each record in the traffic data
        for record in self.traffic_data:
            time = record['timeOfDay']  # Get the time of day from the record (e.g., "14:30")
            junction = record['JunctionName']  # Get the junction name from the record
            hour = int(time.split(":")[0])  # Extract the hour from the time (e.g., 14:30 -> 14)

            # If the junction is in the hourly data, increment the count for that hour and junction
            if junction in hourly_data[hour]:
                hourly_data[hour][junction] += 1

        return hourly_data  # Return the aggregated data



    def find_max_vehicles(self, hourly_data):
        """
        Finds the maximum number of vehicles recorded in any hour across all junctions.
        This helps in scaling the histogram bars based on the highest count.
        
        Returns:
            int: The maximum number of vehicles recorded in any hour.
        """
        # Find the highest count of vehicles in any hour for any junction
        max_vehicles = max(max(hourly_data[hour].values()) for hour in hourly_data)
        return max_vehicles  # Return the maximum number of vehicles


    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars for each hour.
        It visualizes the frequency of vehicles passing through each junction per hour.
        """
        #self.draw_axes()
        hourly_data = self.aggregate_data()  # Get the aggregated data
        max_vehicles = self.find_max_vehicles(hourly_data)  # Get the maximum number of vehicles

        bar_width = 15  # Width of each bar in the histogram
        x_offset = 50  # Starting x position for drawing bars
        y_offset = 550  # y position for the bottom of the bars
        y_scale = 400 / max_vehicles if max_vehicles > 0 else 1  # Scale the bars based on the max vehicles

        # Loop through each hour and draw bars for each junction
        for hour, counts in hourly_data.items():
            x_base = x_offset + hour * (2 * bar_width + 10)  # x position for the bars of this hour

            # Loop through each junction and draw a bar for its vehicle count
            for i, (junction, count) in enumerate(counts.items()):
                bar_height = count * y_scale  # Calculate the height of the bar based on the count
                # Draw the bar for this junction
                self.canvas.create_rectangle(
                    x_base + i * bar_width,  # Left edge of the bar
                    y_offset - bar_height,  # Top edge of the bar
                    x_base + (i + 1) * bar_width,  # Right edge of the bar
                    y_offset,  # Bottom edge of the bar
                    fill="#b2f6a1" if i == 0 else "#e59b9d",  # Green for Elm Avenue, Red for Hanley Highway
                    outline="black"  # Outline color for the bars
                )

                # Add the count value above the bar
                self.canvas.create_text(
                    x_base + i * bar_width + bar_width // 2,  # x position for the text
                    y_offset - bar_height - 10,  # y position for the text
                    text=str(count),  # Display the count value
                    font=("Arial", 8),  # Font style for the text
                    fill="blue" # Color for the text
                )


        # Draw the hour labels at the bottom of the histogram
        for hour in range(24):
            x_pos = x_offset + hour * (2 * bar_width + 10) + bar_width // 2
            self.canvas.create_text(x_pos, 560, text=str(hour).zfill(2))

            
        # Format the date as DD/MM/YYYY
        formatted_date = f"{self.date[:2]}/{self.date[2:4]}/{self.date[4:]}"  # Format date input

        # Draw the title and axis labels
        self.canvas.create_text(
            265, 20, text=f"Histogram of Vehicle Frequency per Hour ({formatted_date})", font=("Arial", 14, "bold")
        )
        self.canvas.create_text(
            515, 592, text="Hours 00:00 to 24:00", font=("Arial", 12)
        )
        self.canvas.create_line(50, 550, 1000, 550, width=2)  # X-axis
        
        
        
    def add_legend(self):
        junction_colors = {'Elm Avenue/Rabbit Road': '#b2f6a1', 'Hanley Highway/Westway': '#e59b9d'}
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        This helps users identify which color represents each junction.
        """
        y = 70
        for junction, color in junction_colors.items():
            self.canvas.create_rectangle(48, y,58, y+10, fill=color)
            self.canvas.create_text(62, y+5, text=junction, anchor='w')
            y += 20
    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        This method initializes the window, draws the histogram, adds the legend, 
        and starts the Tkinter event loop to display the GUI.
        """
        self.setup_window()  # Set up the window and canvas
        self.draw_histogram()  # Draw the histogram
        self.add_legend()  # Add the legend to the histogram
        self.root.mainloop()  # Start the Tkinter main loop




#Task E
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        This class handles loading multiple CSV files, processing the data, 
        and creating the corresponding histograms for each file.
        """
        self.current_data = None  # Store the data loaded from the CSV file

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        This method reads the CSV file, parses it into a list of dictionaries, 
        and stores it for further processing.
        
        Args:
            file_path (str): The path to the CSV file to be loaded.
        
        Returns:
            bool: True if the file is loaded successfully, False if not.
        """
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)  # Read the CSV file into a dictionary
                self.current_data = [row for row in reader]  # Store the rows as a list of dictionaries
            return True  # Return True if the file is loaded successfully
        except FileNotFoundError:
            print(f"File {file_path} not found.")  # Print an error message if the file is not found
            return False  # Return False if the file is not found

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        This ensures that the application starts fresh with each new file.
        """
        self.current_data = None  # Clear the previous data

    def get_user_input(self):
        def is_leap_year(year):
            """
            Checks if a given year is a leap year.
            """
            return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        """
        Prompts the user for the date input in DDMMYYYY format and validates it.
        This method ensures that the date is entered in the correct format before proceeding.
        
        Returns:
            str: The valid date entered by the user.
        """
        day, month, year = None, None, None
        month_names = {2: "February", 4: "April", 6: "June", 9: "September", 11: "November"}
        
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

                # Additional validation for leap years and months with fewer than 31 days
                if month == 2 and day == 29 and not is_leap_year(year):
                    print(f"{year} is not a leap year. Please enter a valid date.")
                    day, month, year = None, None, None
                    continue
                if month == 2 and day == 30:
                    print(f"February does not have 30 days. Please enter a valid date.")
                    day, month, year = None, None, None
                    continue
                if month in {2, 4, 6, 9, 11} and day == 31:
                    print(f"{month_names[month]} does not have 31 days. Please enter a valid date.")
                    day, month, year = None, None, None
                    continue

                date_str = f"{day:02d}{month:02d}{year}"
                return date_str

            except ValueError:
                print("Integer required")
                # Print error if invalid

    def ask_to_continue(self):
        """
        Asks the user if they want to process another file or exit.
        This allows the user to choose whether to continue or stop the program.
        
        Returns:
            str: 'y' if the user wants to continue, 'n' if they want to exit.
        """
        while True:
            continue_choice = input("Do you want to select a data file for a different date, Enter 'Y' or 'N': ").strip().lower()
            # Check if the user input is valid
            if continue_choice in ["y", "n"]:
                return continue_choice  # Return the user's choice
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")  # Print error if invalid

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        This method interacts with the user to load CSV files, display histograms, 
        and ask if they want to continue or exit.
        """
        while True:
            date_input = self.get_user_input()  # Get the date input from the user
            file_path = f"traffic_data{date_input}.csv"  # Construct the file path

            # Try to load the CSV file and create the histogram if successful
            if self.load_csv_file(file_path):
                histogram_app = HistogramApp(self.current_data, date_input)
                histogram_app.run()  # Run the histogram app to display the data

            continue_choice = self.ask_to_continue()  # Ask if the user wants to continue
            if continue_choice == "n":
                print("Exiting program.")  # Exit the program if the user chooses 'n'
                break  # Break the loop to exit
            else:
                self.clear_previous_data()  # Clear the data if the user wants to continue

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        This method continuously processes files based on user input until the user exits.
        """
        self.handle_user_interaction()  # Start the user interaction loop


# Main Program
if __name__ == "__main__":
    processor = MultiCSVProcessor()  # Create an instance of the processor
    processor.process_files()  # Start processing files
