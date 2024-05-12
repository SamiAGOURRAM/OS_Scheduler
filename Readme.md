# CPU Scheduler Simulator

CPU Scheduler Simulator is a web-based application designed to simulate various CPU scheduling algorithms. This application allows users to generate random processes, upload processes from a file, manually input process details, and visualize how different scheduling algorithms manage these processes. The simulator provides insights into different metrics such as average waiting time, average turnaround time, and CPU utilization.

## Features

- **Generate Processes**: Randomly generate a set of processes with configurable parameters.
- **Upload Processes**: Load processes from a file to handle predefined sets of tasks.
- **Manual Input**: Directly input process parameters like arrival times, burst times, and priorities.
- **Scheduling Algorithms**: Support for multiple scheduling algorithms including:
  - First-Come, First-Served (FCFS)
  - Shortest Job First (SJF)
  - Priority Scheduling
  - Round Robin (RR)
  - Priority Round Robin (PRR)
- **Visualization**: Display Gantt charts representing the scheduling order and duration of processes. A table also shows information about each executed process
- **Performance Metrics**: Calculate and display metrics such as average waiting time, average turnaround time, and CPU usage.
- **Comparison**: Plots the different average waiting and turn around time per algorithm

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Handling**: JSON for AJAX communication

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Flask
- A modern web browser


### Running the app

- You can simply access this website : https://samiag.pythonanywhere.com/ and try the scheduling simulator

## Local
- Before running the web app, make sure to install the required packages by running this command :
pip install Flask Werkzeug
- Run the Server: Start the Flask server by running the gui.py script:
                    python gui.py
- Access the Application: Open a web browser and enter the URL provided by the Flask server (typically http://127.0.0.1:5000/).
- Explore: Use the intuitive interface to generate, upload, or manually input processes. Select a scheduling algorithm and observe the results.
- Interact: Experiment with different scheduling algorithms and parameters to understand their effects on process execution and system performance.

## Note
please note that if you wish to test the code in the terminal, you can do so by using the processes.csv and running the test.py. 

Each line in the processes.csv file represents a process with these attributes in order : pid, arrival_time, burst_time, priority(can be empty or any value if working with algorithms that do not take in consideration priorities : rr, fcfs, sjf)



