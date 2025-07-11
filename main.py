import subprocess
import platform
from nlp.nlp_module import NLPModule
from validator.command_validator import CommandValidator
from telemetry.telemetry_agent import TelemetryAgent
from logger.command_history_logger import CommandHistoryLogger
from security.security_classifier import SecurityClassifier
from graph.command_graph import CommandGraph
from telemetry.telemetry_logger import TelemetryLogger

def main(): 
    nlp = NLPModule()
    validator = CommandValidator()
    telemetry = TelemetryAgent()
    history_logger = CommandHistoryLogger()
    security_classifier = SecurityClassifier()
    command_graph = CommandGraph()
    telemetry_logger = TelemetryLogger()

    print("🧠 NeuroShell - AI Terminal Assistant")
    print("Type a natural language command (type 'exit' to quit):")

    while True:
        user_input = input("> ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting.")
            break

        # Translate natural language to shell command
        command = nlp.translate_command(user_input)
        if not command:
            print("❌ Could not generate a shell command.")
            continue

        print(f"→ Shell: {command}")

        # Use NLPModule to execute command with integrated classification and validation
        result = nlp.execute_command(command, user='user')
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            continue

        print(f"→ Output:\n{result['output']}")
        print(f"→ Pre-execution System Stats: {result['pre_stats']}")
        print(f"→ Post-execution System Stats: {result['post_stats']}")
        print(f"→ Command Classification: {result['classification']}")

        # Track usage
        outcome = 'success' if result.get('classification') == 'Safe' else 'fail'
        history_logger.log_command(command, outcome)
        command_graph.add_command(command)
        telemetry_logger.log_usage()

        # Show telemetry log summary
        telemetry_data = telemetry_logger.get_telemetry_data()
        print(f"→ Telemetry Data: {telemetry_data}")

        # Print command graph and history
        print(f"→ Execution Order: {command_graph.get_execution_order()}")
        print(f"→ Command History: {history_logger.get_history()}")

if __name__ == "__main__":
    main()
