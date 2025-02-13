import docker
from flask import Flask
from prettytable import PrettyTable
app = Flask(__name__)
client = docker.from_env()
@app.route('/')
def get_cpu_utilization():
    containers = client.containers.list()
    processes = []
    for container in containers:
        container_name = container.name
        container_stats = container.stats(stream=False)
        cpu_percent = container_stats['cpu_stats']['cpu_usage']['total_usage'] / container_stats['cpu_stats']['system_cpu_usage'] * 100
        processes.append((container_name, cpu_percent))
    # Calculate the total CPU usage across all containers
    total_cpu_percent = sum(cpu_percent for _, cpu_percent in processes)
    # Scale the CPU utilization values to a percentage out of 100
    scaled_processes = [(container_name, cpu_percent / total_cpu_percent * 100) for container_name, cpu_percent in processes]
    table = PrettyTable(['Container', 'CPU %'])
    table.align['Container'] = 'l'
    table.align['CPU %'] = 'r'
    for process in scaled_processes:
        table.add_row(process)
    return table.get_html_string(sortby='CPU %', reversesort=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)