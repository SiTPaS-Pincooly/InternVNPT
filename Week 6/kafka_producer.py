# Producer ver 2.
import pandas as pd
import json
import time
from kafka import KafkaProducer

# ---------------------------------------------------------------------------
# CONFIG — adjust these to control the test
# ---------------------------------------------------------------------------
TOPIC = "network-events"
REPEATS = 10         # how many times to loop through the whole CSV
SLEEP_BETWEEN_SENDS = 0   # seconds; set to 0 for max throughput, e.g. 0.01 to cap ~100/sec
REPORT_EVERY = 10000     # print a rate update every N messages sent

# ---------------------------------------------------------------------------
# PRODUCER SETUP — tuned for throughput
# ---------------------------------------------------------------------------
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=20,          # wait up to 20ms to batch more messages per network request
    batch_size=65536,       # larger internal batch size (bytes), fewer round-trips
    compression_type="lz4",  # compress batches before sending — less network I/O
    acks=1,                    # don't wait for full replication ack; fine for local single-broker testing
)

# ---------------------------------------------------------------------------
# LOAD DATA ONCE, PRE-CONVERTED TO PLAIN DICTS
# ---------------------------------------------------------------------------
df = pd.read_csv("netflix_titles.csv")
records = df.where(pd.notnull(df), None).to_dict(orient="records")
print(f"Loaded {len(records)} rows from CSV. Will send {REPEATS}x = {len(records) * REPEATS} total messages.")

# ---------------------------------------------------------------------------
# SEND LOOP
# ---------------------------------------------------------------------------
start = time.time()
count = 0

for r in range(REPEATS):
    for message in records:
        producer.send(TOPIC, message)
        count += 1

        if SLEEP_BETWEEN_SENDS:
            time.sleep(SLEEP_BETWEEN_SENDS)

        if count % REPORT_EVERY == 0:
            elapsed = time.time() - start
            print(f"Sent {count} rows | elapsed {elapsed:.1f}s | actual rate: {count / elapsed:.1f} rows/sec")

# only flush once, at the very end — forces delivery of anything still buffered
producer.flush()

elapsed = time.time() - start
print(f"\nDone. Sent {count} rows across {REPEATS} passes in {elapsed:.1f}s "
      f"(overall avg: {count / elapsed:.1f} rows/sec)")
