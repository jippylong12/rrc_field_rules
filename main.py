from src.infrastructure import OracleContainer
from src.parser import DataSyncer
import sys

def main():
    infra = OracleContainer()
    syncer = DataSyncer()

    try:
        # 1. Start Infrastructure 
        # (This now waits for "AUTOMATED SETUP COMPLETE" in the logs)
        infra.start()

        # 2. Sync to Mongo
        # We don't need to run import here anymore, Docker did it.
        syncer.sync_all_tables()

    except Exception as e:
        print(f"❌ Fatal Error: {e}")
    finally:
        # 4. Cleanup 
        # infra.stop() # Uncomment this if you want it to shut down automatically
        pass

if __name__ == "__main__":
    main()