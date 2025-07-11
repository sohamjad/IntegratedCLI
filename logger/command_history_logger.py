import datetime

class CommandHistoryLogger:
    def __init__(self):
        self.history = []

    def log_command(self, command, outcome):
        timestamp = datetime.datetime.now()
        self.history.append({'command': command, 'timestamp': timestamp, 'outcome': outcome})

    def get_history(self):
        return self.history

