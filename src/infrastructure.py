import subprocess
import time

class OracleContainer:
    def __init__(self, compose_file="docker/docker-compose.yml"):
        self.compose_file = compose_file

    def start(self):
        print("🚀 Starting Oracle Container...")
        subprocess.run(["docker-compose", "-f", self.compose_file, "up", "-d"], check=True)
        self._wait_for_import_completion()

    def stop(self):
        print("🛑 Shutting down Oracle Container...")
        subprocess.run(["docker-compose", "-f", self.compose_file, "down"], check=True)

    def _wait_for_import_completion(self):
        """Polls the Docker logs to ensure the legacy import script has finished."""
        print("⏳ Waiting for legacy import to finish (this happens inside the container)...")
        container_name = "rrc_oracle_parser"
        
        for _ in range(60):  # Wait up to 10 minutes
            # Check container logs for our success message
            result = subprocess.run(
                ["docker", "logs", container_name],
                capture_output=True, text=True
            )
            
            # This is the string we echoed in init_oracle.sh
            if "AUTOMATED SETUP COMPLETE" in result.stdout:
                print("✅ Database is ready and Data is Imported!")
                return
            
            time.sleep(10)
        
        raise TimeoutError("Oracle DB came up, but the data import script timed out.")