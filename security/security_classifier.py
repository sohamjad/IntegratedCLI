class SecurityClassifier:
    def __init__(self):
        # Basic classification setup
        self.safe_commands = {'ls', 'echo', 'dir'}
        self.dangerous_commands = {'rm', 'del', 'shutdown'}

    def classify_command(self, command):
        if any(cmd in command for cmd in self.dangerous_commands):
            return 'dangerous'
        elif any(cmd in command for cmd in self.safe_commands):
            return 'safe'
        else:
            return 'unknown'

    def suggest_safer_alternatives(self, command):
        if command in self.dangerous_commands:
            return 'Consider using safer alternatives such as backups or confirmations.'
        return 'No safer alternative suggested.'
