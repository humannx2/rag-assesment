import pandas as pd
import random
from datetime import datetime, timedelta

def generate_telemetry_data(
    num_servers=5,
    days=7,
    entries_per_hour=4,
    output_file="telemetry.csv"
):
    servers = [f"server_{i}" for i in range(1, num_servers + 1)]
    now = datetime.now()
    delta = timedelta(hours=1 / entries_per_hour)
    timestamps = [now - i * delta for i in range(days * 24 * entries_per_hour)]

    data = []
    for timestamp in timestamps:
        for server in servers:
            cpu = round(random.uniform(5, 100), 2)
            memory = round(random.uniform(10, 100), 2)
            disk = round(random.uniform(20, 100), 2)
            data.append([timestamp, server, cpu, memory, disk])

    df = pd.DataFrame(data, columns=["timestamp", "server", "cpu", "memory", "disk"])
    df.to_csv(output_file, index=False)
    print(f" Generated {len(df)} rows of telemetry data in {output_file}")

if __name__ == "__main__":
    generate_telemetry_data()
