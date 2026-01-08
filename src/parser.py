import oracledb
import pymongo
import pandas as pd
import time

class DataSyncer:
    def __init__(self):
        self.oracle_user = "PROD_OG_OWNR"
        self.oracle_pwd = "ParserPassword123"
        self.oracle_dsn = "localhost:1521/FREEPDB1"
        self.mongo_uri = "mongodb://localhost:27017/"

    def _connect_to_oracle(self):
        """Attempts connection with retries for listener delays."""
        retries = 15
        for i in range(retries):
            try:
                conn = oracledb.connect(
                    user=self.oracle_user, 
                    password=self.oracle_pwd, 
                    dsn=self.oracle_dsn
                )
                return conn
            except oracledb.Error as e:
                error_str = str(e)
                # DPY-6001 / ORA-12514 mean the DB is up, but the service isn't registered yet.
                if "DPY-6001" in error_str or "ORA-12514" in error_str:
                    print(f"⏳ Oracle Listener not ready for FREEPDB1 yet... Retrying ({i+1}/{retries})")
                    time.sleep(5)
                else:
                    # If it's a wrong password or other error, fail immediately
                    raise e
        
        raise TimeoutError("❌ timed out waiting for Oracle Service FREEPDB1 to register.")

    def sync_all_tables(self, target_db_name="rrc_field_rules"):
        # 1. Connect to Oracle (using the new retry logic)
        print("🔌 Connecting to Oracle...")
        try:
            p_conn = self._connect_to_oracle()
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return

        # 2. Connect to Mongo
        m_client = pymongo.MongoClient(self.mongo_uri)
        db = m_client[target_db_name]

        # 3. Get list of tables belonging to PROD_OG_OWNR
        print("🔍 Scanning tables...")
        tables_query = "SELECT table_name FROM user_tables"
        
        tables = pd.read_sql(tables_query, p_conn)
        
        if tables.empty:
            print("⚠️ Connected, but found no tables! Import might have failed or user is empty.")
            p_conn.close()
            return

        for table in tables['TABLE_NAME']:
            print(f"🔄 Syncing table: {table}")
            self._copy_table(p_conn, db, table)
            
        p_conn.close()
        print("🎉 All data synced to MongoDB.")

    def _copy_table(self, oracle_conn, mongo_db, table_name):
        query = f"SELECT * FROM {table_name}"
        
        try:
            # Chunksize helps prevent memory issues with large tables
            for chunk in pd.read_sql(query, oracle_conn, chunksize=5000):
                data = chunk.to_dict(orient='records')
                if data:
                    mongo_db[table_name].insert_many(data)
        except Exception as e:
            print(f"⚠️ Error syncing {table_name}: {e}")