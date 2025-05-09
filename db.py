import duckdb
import os

def load_csv_to_duckdb(csv_file='telemetry.csv', db_file='telemetry.duckdb', table_name='telemetry'):
    # Connect to duckdb
    con = duckdb.connect(database=db_file)

    # loading csv into duckdb
    con.execute(f"""
        CREATE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_file}')
    """)

    print(f"✅ Data from '{csv_file}' loaded into '{db_file}' as table '{table_name}'.")

    # show a sample
    sample = con.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf()
    print("\n📋 Sample data:\n", sample)

    con.close()

if __name__ == "__main__":
    if not os.path.exists("telemetry.csv"):
        print("telemetry.csv not found. Please run the simulation script first.")
    else:
        load_csv_to_duckdb()
