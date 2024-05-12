from flask import Flask, render_template, request, jsonify
from input import generate_random_processes, read_processes_from_file
from process import Process
from werkzeug.utils import secure_filename
import os


from fcfsScheduler import fcfsScheduler
from sjfScheduler import sjfScheduler
from RoundRobinScheduler import RoundRobinSheduler
from priorityScheduler import priorityScheduler
from PriorityRoundRobinScheduler import PriorityRoundRobinScheduler




            
def build_scheduler(type, quantum=4):
    if type == "fcfs":
        scheduler = fcfsScheduler()
    elif type == "sjf":
        scheduler = sjfScheduler()
    elif type == "priority":
        scheduler = priorityScheduler()
    elif type == "round_robin":
        scheduler = RoundRobinSheduler(quantum)
        scheduler.quantum = quantum
    elif type == "priority_round_robin":
        scheduler = PriorityRoundRobinScheduler(quantum)
        scheduler.quantum = quantum
    else:
        raise Exception("Scheduling algorithm not recognized")
    
    return scheduler

def compute_average( processes):
        avg_waiting_time = 0
        avg_turntaround_time = 0
    
        for i in range(len(processes)):
            avg_waiting_time += processes[i].waiting_time
            avg_turntaround_time += processes[i].turnAround_time

        return avg_waiting_time/len(processes), avg_turntaround_time/len(processes)

def compute_cpu_usage(gantt_chart):
    total_time = 0
    active_time = 0

    # Assuming gantt_chart is a dictionary with tuples as keys (start, end) and values are either 'idle' or Process objects
    last_end_time = 0
    for (start, end), process in gantt_chart.items():
        if last_end_time < end:
            last_end_time = end  # Update last end time to the maximum found
        if process != 'idle':
            active_time += (end - start)  # Sum up all non-idle durations

    total_time = last_end_time  # Total time from 0 to last process end time

    if total_time == 0:  # Avoid division by zero
        return 0

    cpu_usage = (active_time / total_time) * 100
    return cpu_usage
    

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')


@app.route('/manual_input', methods=['POST'])
def manual_input():
    """
    Receive manual input for processes.

    Returns:
        json: JSON response containing the processes.
    """
    processes_data = request.get_json()
    # Assuming you're creating a Process object for each entry
    processes = [Process(pid=p['pid'], arrival_time=p['arrival_time'], burst_time=p['burst_time'], priority=p['priority']) for p in processes_data]
    # Return the processes as JSON
    return jsonify([process.__dict__ for process in processes])








@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate random processes.

    Returns:
        json: JSON response containing the randomly generated processes.
    """
    data = request.get_json()
    num_processes = int(data['num_processes'])
    burst_time_min = int(data['burst_min'])
    burst_time_max = int(data['burst_max'])
    arrival_time_min = int(data['arrival_min'])
    arrival_time_max = int(data['arrival_max'])
    priority_range = data.get('priority_range', None)
    if priority_range:
        priority_min, priority_max = map(int, priority_range.split(','))
        priority_range = (priority_min, priority_max)
    processes = generate_random_processes(num_processes, (burst_time_min, burst_time_max), (arrival_time_min, arrival_time_max), priority_range)
    return jsonify([process.__dict__ for process in processes])



@app.route('/upload', methods=['POST'])
def upload():
    """
    Upload a file containing processes.

    Returns:
        json: JSON response containing the processes read from the file.
    """
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Use the configured upload folder
        file.save(filepath)  # Save the file to the path
        processes = read_processes_from_file(filepath)  # Assuming this function can handle the full path

        return jsonify([process.__dict__ for process in processes])
    else:
        return jsonify({'error': 'Invalid file or no file uploaded'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

@app.route('/benchmark', methods=['POST'])
def benchmark():
    """
    Benchmark different scheduling algorithms.

    Returns:
        json: JSON response containing the benchmark results.
    """
    data = request.get_json()
    processes_data = data['processes']
    quantum = int(data["quantum"])
    algorithms = ['fcfs', 'sjf', 'priority', 'round_robin', 'priority_round_robin']
    results = {}

    for algorithm in algorithms:
        procs = [Process(proc['pid'], proc['arrival_time'], proc['burst_time'], proc['priority']) for proc in processes_data]
        for proc in procs:
            proc.reset()

        scheduler = build_scheduler(algorithm, quantum)
        scheduler.schedule(procs)
        avg_waiting_time, avg_turnaround_time = compute_average(procs)

        results[algorithm] = {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        }
    print(results)

    return jsonify(results)


@app.route('/schedule', methods=['POST'])


def schedule():
    """
    Schedule processes using the specified algorithm.

    Returns:
        json: JSON response containing the scheduling results.
    """
    data = request.get_json()
    algorithm = data['algorithm']
    processes_data = data['processes']
    procs = [Process(proc['pid'], proc['arrival_time'], proc['burst_time'], proc['priority']) for proc in processes_data]
    print("Before reset:", [(p.pid, p.waiting_time, p.is_complete) for p in procs])
    for proc in procs:
        proc.reset()
    print("After reset:", [(p.pid, p.waiting_time, p.is_complete) for p in procs])
    time_quantum = int(data.get('time_quantum', 4))

    scheduler = build_scheduler(algorithm, time_quantum)
    
    scheduler.schedule(procs)
    print("After scheduling:", [(p.pid, p.waiting_time, p.is_complete) for p in procs])
    avg_waiting_time , avg_turntaround_time = compute_average(procs)
    
    gant_chart = scheduler.gant_chart
    scheduled_order  = [process.pid for process in gant_chart.values() if isinstance(process, Process)]
    

    formatted_gantt_chart = [
        {
            'start': start,
            'end': end,
            'processId': process.pid if isinstance(process, Process) else None,
            'state': 'idle' if process == 'idle' else 'active'
        } for (start, end), process in gant_chart.items()
    ]
    cpu_usage = compute_cpu_usage(gant_chart)

    # Prepare data to send back to the client
    result = {
        'algorithm': algorithm,
        'scheduled_order': scheduled_order,
        'avg_waiting_time': avg_waiting_time,
        'avg_turnaround_time': avg_turntaround_time,
        'processes': [proc.__dict__ for proc in procs],
        "gantt_chart" : formatted_gantt_chart,
        "cpu_usage" :  cpu_usage  # Sending back the original process data as well
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
