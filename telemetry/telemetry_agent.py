import psutil

class TelemetryAgent:
    def get_system_stats(self):
        return {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent
        }

