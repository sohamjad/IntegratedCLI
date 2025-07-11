import os
os.environ["TRANSFORMERS_NO_TF"] = "1"  # Force PyTorch-only backend

from transformers import pipeline
import platform
import subprocess
import datetime
import json
import psutil

class NLPModule:
    def __init__(self):
        self.nlp_pipeline = pipeline(
            "text2text-generation",
            model="alexsha/t5-large-finetuned-English-to-BASH",
            tokenizer="alexsha/t5-large-finetuned-English-to-BASH",
            trust_remote_code=True,
            device=-1  # Use 0 if GPU is available
        )

    def detect_os(self):
        os_name = platform.system().lower()
        if 'windows' in os_name:
            return 'windows'
        elif 'darwin' in os_name:
            return 'macos'
        elif 'linux' in os_name:
            return 'linux'
        else:
            return 'unknown'

    def translate_command(self, user_input):
        try:
            result = self.nlp_pipeline(user_input, max_new_tokens=100)
            if not result or 'generated_text' not in result[0]:
                raise ValueError("No valid output from model.")
            command = result[0]['generated_text'].strip()

            os_type = self.detect_os()

            # Simple cross-platform command mapping
            if os_type == 'windows':
                if command.startswith("ls"):
                    return "dir"
                if command.startswith("clear"):
                    return "cls"
                if "mkdir" in command:
                    return command.replace("mkdir", "mkdir")  # No-op, for future mapping

            return command
        except Exception as e:
            print(f"⚠️ Model output invalid or incorrect.\nError: {e}")
            return None

    def classify_command(self, command):
        dangerous_patterns = ["rm -rf", "mkfs", ":(){:|:&};:"]
        return "Dangerous" if any(p in command for p in dangerous_patterns) else "Safe"

    def log_command(self, command, user, output):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user,
            "command": command,
            "output": output
        }
        with open("command_history.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def get_system_stats(self):
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent
        }

    def execute_command(self, command, user="unknown"):
        pre_stats = self.get_system_stats()
        classification = self.classify_command(command)
        if classification == "Dangerous":
            return {"error": "Command classified as dangerous and blocked."}

        try:
            output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output

        post_stats = self.get_system_stats()
        self.log_command(command, user, output)

        return {
            "output": output,
            "pre_stats": pre_stats,
            "post_stats": post_stats,
            "classification": classification,
            "command_graph_node": {"command": command, "status": "executed"}
        }
