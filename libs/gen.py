#!/usr/bin/env python

import random
import confluent_kafka.avro
import uuid
import sys
import time

# gen.py 1000000 schema-registry-host broker-host 0 orders client-id-1

COUNT = int(sys.argv[1])
SCHEMA_REGISTRY= sys.argv[2]
BROKER = sys.argv[3]
SEED = int(sys.argv[4])
TOPIC = sys.argv[5]
CLIENT_ID = sys.argv[6]

if __name__ == '__main__':

    # no need to set seed after all...
    rnd = random.Random()
    tbl = bytes.maketrans(
        bytearray(range(256)),
        bytearray([ord(b'a') + b % 26 for b in range(256)]))
    
    key_schema_string = """
    {"type": "string"}
    """
    avro_schema_string = """
        {
        "connect.name": "orders",
        "fields": [
            {
            "name": "acc_loc",
            "type": "string"
            },
            {
            "name": "acc_num",
            "type": "string"
            },
            {
            "name": "ts",
            "type": {
                "connect.name": "org.apache.kafka.connect.data.Timestamp",
                "connect.version": 1,
                "logicalType": "timestamp-millis",
                "type": "long"
            }
            },
            {
            "name": "c_ts",
            "type": "long"
            },
            {
            "name": "send_timestamp",
            "type": {
                "connect.name": "org.apache.kafka.connect.data.Timestamp",
                "connect.version": 1,
                "logicalType": "timestamp-millis",
                "type": "long"
            }
            },
            {
            "name": "user_id",
            "type": "string"
            },
            {
            "name": "quantity",
            "type": "long"
            },
            {
            "name": "side",
            "type": "string"
            },
            {
            "name": "price",
            "type": "double"
            },
            {
            "name": "is_contra",
            "type": "boolean"
            },
            {
            "name": "symbol",
            "type": "string"
            },
            {
            "name": "col001",
            "type": "string"
            },
            {
            "name": "col002",
            "type": "string"
            },
            {
            "name": "col003",
            "type": "string"
            },
            {
            "name": "col004",
            "type": "string"
            },
            {
            "name": "col005",
            "type": "string"
            },
            {
            "name": "col006",
            "type": "string"
            },
            {
            "name": "col007",
            "type": "string"
            },
            {
            "name": "col008",
            "type": "string"
            },
            {
            "name": "col009",
            "type": "string"
            },
            {
            "name": "col010",
            "type": "string"
            },
            {
            "name": "col011",
            "type": "string"
            },
            {
            "name": "col012",
            "type": "string"
            },
            {
            "name": "col013",
            "type": "string"
            },
            {
            "name": "col014",
            "type": "string"
            },
            {
            "name": "col015",
            "type": "string"
            },
            {
            "name": "col016",
            "type": "string"
            },
            {
            "name": "col017",
            "type": "string"
            },
            {
            "name": "col018",
            "type": "string"
            },
            {
            "name": "col019",
            "type": "string"
            },
            {
            "name": "col020",
            "type": "string"
            },
            {
            "name": "col101",
            "type": "long"
            },
            {
            "name": "col102",
            "type": "long"
            },
            {
            "name": "col103",
            "type": "long"
            },
            {
            "name": "col104",
            "type": "long"
            },
            {
            "name": "col105",
            "type": "long"
            },
            {
            "name": "col106",
            "type": "long"
            },
            {
            "name": "col107",
            "type": "long"
            },
            {
            "name": "col108",
            "type": "long"
            },
            {
            "name": "col109",
            "type": "long"
            },
            {
            "name": "col110",
            "type": "long"
            },
            {
            "name": "col111",
            "type": "long"
            },
            {
            "name": "col112",
            "type": "long"
            },
            {
            "name": "col113",
            "type": "long"
            },
            {
            "name": "col114",
            "type": "long"
            },
            {
            "name": "col115",
            "type": "long"
            },
            {
            "name": "col116",
            "type": "long"
            },
            {
            "name": "col117",
            "type": "long"
            },
            {
            "name": "col118",
            "type": "long"
            },
            {
            "name": "col119",
            "type": "long"
            },
            {
            "name": "col120",
            "type": "long"
            },
            {
            "name": "col201",
            "type": "boolean"
            },
            {
            "name": "col202",
            "type": "boolean"
            },
            {
            "name": "col203",
            "type": "boolean"
            },
            {
            "name": "col204",
            "type": "boolean"
            },
            {
            "name": "col205",
            "type": "boolean"
            },
            {
            "name": "col206",
            "type": "boolean"
            },
            {
            "name": "col207",
            "type": "boolean"
            },
            {
            "name": "col208",
            "type": "boolean"
            },
            {
            "name": "col209",
            "type": "boolean"
            },
            {
            "name": "col210",
            "type": "boolean"
            },
            {
            "name": "col211",
            "type": "boolean"
            },
            {
            "name": "col212",
            "type": "boolean"
            },
            {
            "name": "col213",
            "type": "boolean"
            },
            {
            "name": "col214",
            "type": "boolean"
            },
            {
            "name": "col215",
            "type": "boolean"
            },
            {
            "name": "col216",
            "type": "boolean"
            },
            {
            "name": "col217",
            "type": "boolean"
            },
            {
            "name": "col218",
            "type": "boolean"
            },
            {
            "name": "col219",
            "type": "boolean"
            },
            {
            "name": "col220",
            "type": "boolean"
            }
        ],
        "name": "orders",
        "namespace": "orders",
        "type": "record"
        }
    """

    key_schema = confluent_kafka.avro.loads(key_schema_string)
    value_schema = confluent_kafka.avro.loads(avro_schema_string)


    config = {
        'bootstrap.servers': f'{BROKER}:9092',
        'schema.registry.url': f'http://{SCHEMA_REGISTRY}:8081',
        'client.id': CLIENT_ID
            }

    # Create Producer instance
    producer = confluent_kafka.avro.AvroProducer(
        config, 
        default_key_schema=key_schema, 
        default_value_schema=value_schema)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        # else:
        #     print(msg.topic(), msg.key().decode('utf-8')[6:] )

            
    for _ in range(COUNT):
            
        k = str(uuid.UUID(int=rnd.getrandbits(128)))
        v: dict = {}
        
        v["acc_loc"] = str(rnd.choice([123, 354, 3451, 312, 23, 51, 23, 8123, 8354, 83451, 8312, 823, 851, 823]))
        v["acc_num"] = 'A-' + str(rnd.randint(10, 1e9)).zfill(10)
        v["ts"] = rnd.randint(1609459200000,1672600083000) # between ~2020-12-31 and ~2023-01-01
        v["c_ts"] = rnd.randint(0, 100)
        v["send_timestamp"] = time.time() * 1000 # dt.datetime.utcnow()
        v["user_id"] = 'System'
        v["quantity"] = rnd.randint(0, 1000000)
        v["side"] = rnd.choice(['buy', 'sell'])
        v["price"] = round(rnd.uniform(10, 1e6), 2)
        v["is_contra"] = rnd.choice([True, False])
        v["symbol"] = 'SYM-' + str(rnd.randint(1000, 9999))
        v["col001"] = rnd.getrandbits(8*14).to_bytes(14, 'big').translate(tbl).decode()
        v["col002"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col003"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col004"] = rnd.getrandbits(8*13).to_bytes(13, 'big').translate(tbl).decode()
        v["col005"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col006"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col007"] = rnd.getrandbits(8* 3).to_bytes( 3, 'big').translate(tbl).decode()
        v["col008"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col009"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col010"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col011"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col012"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col013"] = rnd.getrandbits(8* 5).to_bytes( 5, 'big').translate(tbl).decode()
        v["col014"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col015"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col016"] = rnd.getrandbits(8*12).to_bytes(12, 'big').translate(tbl).decode()
        v["col017"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col018"] = rnd.getrandbits(8*15).to_bytes(15, 'big').translate(tbl).decode()
        v["col019"] = rnd.getrandbits(8*10).to_bytes(10, 'big').translate(tbl).decode()
        v["col020"] = rnd.getrandbits(8*11).to_bytes(11, 'big').translate(tbl).decode()
        v["col101"] = rnd.randint(0, 1e10)
        v["col102"] = rnd.randint(0, 1e10)
        v["col103"] = rnd.randint(0, 1e10)
        v["col104"] = rnd.randint(0, 1e10)
        v["col105"] = rnd.randint(0, 1e10)
        v["col106"] = rnd.randint(0, 1e12)
        v["col107"] = rnd.randint(0, 1e10)
        v["col108"] = rnd.randint(0, 1e10)
        v["col109"] = rnd.randint(0, 1e10)
        v["col110"] = rnd.randint(0, 1e10)
        v["col111"] = rnd.randint(0, 1e10)
        v["col112"] = rnd.randint(0, 1e10)
        v["col113"] = rnd.randint(0, 1e10)
        v["col114"] = rnd.randint(0, 1e10)
        v["col115"] = rnd.randint(0, 1e14)
        v["col116"] = rnd.randint(0, 1e10)
        v["col117"] = rnd.randint(0, 1e10)
        v["col118"] = rnd.randint(0, 1e10)
        v["col119"] = rnd.randint(0, 1e10)
        v["col120"] = rnd.randint(0, 1e16)
        v["col201"] = rnd.choice([True, False])
        v["col202"] = rnd.choice([True, False])
        v["col203"] = rnd.choice([True, False])
        v["col204"] = rnd.choice([True, False])
        v["col205"] = rnd.choice([True, False])
        v["col206"] = rnd.choice([True, False])
        v["col207"] = rnd.choice([True, False])
        v["col208"] = rnd.choice([True, False])
        v["col209"] = rnd.choice([True, False])
        v["col210"] = rnd.choice([True, False])
        v["col211"] = rnd.choice([True, False])
        v["col212"] = rnd.choice([True, False])
        v["col213"] = rnd.choice([True, False])
        v["col214"] = rnd.choice([True, False])
        v["col215"] = rnd.choice([True, False])
        v["col216"] = rnd.choice([True, False])
        v["col217"] = rnd.choice([True, False])
        v["col218"] = rnd.choice([True, False])
        v["col219"] = rnd.choice([True, False])
        v["col220"] = rnd.choice([True, False])
    
    
        # Trigger any available delivery report callbacks from previous produce() calls
        producer.poll(0)       
        producer.produce(topic=TOPIC, key=k, value=v, callback=delivery_callback)


    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
    producer.flush()
    