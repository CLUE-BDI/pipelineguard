import json
from kafka import KafkaProducer

KAFKA_BROKER = "localhost:9092"
TOPIC = "pipelineguard.findings"

def main():
    with open("outputs/normalized_findings.json", "r", encoding="utf-8") as f:
        payload = json.load(f)

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    producer.send(TOPIC, payload)
    producer.flush()
    print(f"Published findings to topic: {TOPIC}")

if __name__ == "__main__":
    main()