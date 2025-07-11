class CommandValidator:
    def __init__(self):
        self.dangerous_patterns = ["rm -rf /", "mkfs", ":(){:|:&};:"]

    def is_safe(self, command):
        for pattern in self.dangerous_patterns:
            if pattern in command:
                return False
        return True

