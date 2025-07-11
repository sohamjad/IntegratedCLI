import psutil

class TelemetryLogger:
    def __init__(self):
        self.data = []

    def log_usage(self):
        # Log current CPU and memory usage
        usage = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent
        }
        self.data.append(usage)

    def get_telemetry_data(self):
        return self.data
