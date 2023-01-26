# Kafka 2 CockroachDB via JDBC Sink Connector

## Test Infrastructure and Component Setup

Infrastructure was deployed using Ansible on Google Cloud VMs:

- Single node Confluent Platform (Kafka broker) on a `n2-standard-16` instance type.
- 3 nodes CockroachDB cluster using first the `n2-standard-8` type, and later the `n2-standard-16` instance type.
  The VM was provisioned with 4 locally attached NVME SSDs.

The main Kafka backend was installed using the [Ansible Playbooks for Confluent Platform](https://docs.confluent.io/ansible/current/overview.html).

The CockroachDB cluster and the HAProxy load balancer instance that sits in front of the nodes were installed using the [fabiog1901.cockroachdb Ansible Collection](https://github.com/fabiog1901/cockroachdb-collection).

### Kafka Producer

To load data into the Kafka Topic we used a simple generator written in Python, `gen.py`, available in the `libs` folder.
The generator leverages the `confluent-kafka` [package](https://github.com/confluentinc/confluent-kafka-python) for publishing Avro records of about 60 fields.
The generator is started and let run for 5 minutes before any consumer process is started, so that the Topic is always well filled with records.

### Kafka Consumer

Kafka Connect was configured with the [JDBC Sink Connector](https://docs.confluent.io/kafka-connectors/jdbc/current/sink-connector/overview.html), however, a custom `kafka-connect-jdbc-10.6.1.jar` file was used: the only change made to the original version was to set `autocommit=true` for the SQL transactions, [here](https://github.com/confluentinc/kafka-connect-jdbc/blob/v10.6.1/src/main/java/io/confluent/connect/jdbc/sink/JdbcDbWriter.java#L57).
This change is important as it allows statements to be executed implicitly, saving therefore a roundtrip for the commit message.

Similarly, a custom [PostgreSQL JDBC Driver](https://jdbc.postgresql.org/) was used, allowing for batch statements to be larger than 128 records, see [here](https://github.com/pgjdbc/pgjdbc/blob/REL42.5.0/pgjdbc/src/main/java/org/postgresql/jdbc/PgPreparedStatement.java#L1726).
The result is we can now test with multi-value INSERT statements that have more than 128 values.

## CockroachDB Cluster

The CockroachDB cluster runs version 22.2.2 with the default settings. The database was seeded with approximately 0.5TB of data.
The data was generated externally and imported from Google Cloud Storage directly into the database.

## Test Description

We tested with 2 different instance types (8 and 16 vCPUs instances) and with multiple Topic partition and batch sizes.
Script `play.py` shows roughly the test workflow (partitions were adjusted when testing on the 16 vcpu node cluster).
In short, for both the 8 and 16 vcpus node clusters, we cycled through all partitions, and for each partition, we cycled through all batch sizes.

On each **partition** cycle, the JDBC Sink Connector was created with `tasks.max` set to the same number as the partition count.
Here, a _task_ is a process that creates a database connection, consumes records from the assigned topic partition, prepares the INSERT statement and finally sends it to CockroachDB for execution.

On each **batch size** cycle, the JDBC Sink Connector was created with `batch.size` and `consumer.override.max.poll.records` set to the current value.

Results of latency, throughput (TPS) and CPU util are shown below.
`CPUs` show the total number of vCPUs for the entire cluster.

| CPUs | Partitions/connections | batch.size | TPS   | CPU | latency_ms |
| ---- | ---------------------- | ---------- | ----- | --- | ---------- |
| 24   | 6                      | 16         | 2126  | 20  | 40         |
| 24   | 6                      | 32         | 3375  | 20  | 51         |
| 24   | 6                      | 64         | 5048  | 25  | 65         |
| 24   | 6                      | 128        | 6329  | 30  | 100        |
| 24   | 6                      | 256        | 8788  | 35  | 144        |
| 24   | 6                      | 512        | 10717 | 40  | 218        |
| 24   | 6                      | 1024       | 12765 | 35  | 379        |
| 24   | 18                     | 16         | 4004  | 45  | 63         |
| 24   | 18                     | 32         | 6108  | 50  | 88         |
| 24   | 18                     | 64         | 8660  | 60  | 122        |
| 24   | 18                     | 128        | 11658 | 65  | 172        |
| 24   | 18                     | 256        | 14164 | 70  | 265        |
| 24   | 18                     | 512        | 15847 | 80  | 428        |
| 24   | 18                     | 1024       | 18520 | 75  | 766        |
| 24   | 54                     | 16         | 6886  | 65  | 111        |
| 24   | 54                     | 32         | 9621  | 75  | 168        |
| 24   | 54                     | 64         | 11865 | 80  | 261        |
| 24   | 54                     | 128        | 13206 | 85  | 443        |
| 24   | 54                     | 256        | 14370 | 85  | 732        |
| 24   | 54                     | 512        | 14906 | 85  | 1100       |
| 24   | 54                     | 1024       | 16083 | 85  | 2100       |
| 48   | 18                     | 16         | 5608  | 20  | 45         |
| 48   | 18                     | 32         | 8121  | 20  | 61         |
| 48   | 18                     | 64         | 10606 | 25  | 88         |
| 48   | 18                     | 128        | 15464 | 35  | 116        |
| 48   | 18                     | 256        | 19751 | 40  | 165        |
| 48   | 18                     | 512        | 21649 | 50  | 261        |
| 48   | 54                     | 16         | 9542  | 40  | 83         |
| 48   | 54                     | 32         | 13285 | 45  | 118        |
| 48   | 54                     | 64         | 17597 | 50  | 165        |
| 48   | 54                     | 128        | 21043 | 55  | 282        |
| 48   | 54                     | 256        | 21123 | 55  | 546        |
| 48   | 54                     | 512        | 22658 | 55  | 846        |
| 48   | 96                     | 16         | 12576 | 50  | 114        |
| 48   | 96                     | 32         | 16357 | 55  | 173        |
| 48   | 96                     | 64         | 19157 | 55  | 282        |
| 48   | 96                     | 128        | 19895 | 55  | 553        |
| 48   | 96                     | 256        | 20185 | 55  | 1100       |
| 48   | 96                     | 512        | 18830 | 55  | 1900       |
| 48   | 162                    | 16         | 13869 | 55  | 171        |
| 48   | 162                    | 32         | 18161 | 55  | 262        |
| 48   | 162                    | 64         | 18495 | 55  | 498        |
| 48   | 162                    | 128        | 19117 | 55  | 994        |
| 48   | 162                    | 256        | 18387 | 55  | 2000       |
| 48   | 162                    | 512        | 16151 | 55  | 3600       |

## References

- [Ansible Playbooks for Confluent Platform](https://docs.confluent.io/ansible/current/overview.html)
- [fabiog1901.cockroachdb Ansible Collection](https://github.com/fabiog1901/cockroachdb-collection)
- [JDBC Sink Connector](https://docs.confluent.io/kafka-connectors/jdbc/current/sink-connector/overview.html)
- [Confluent's Python Client confluent-kafka](https://github.com/confluentinc/confluent-kafka-python)
- [PostgreSQL JDBC Driver](https://jdbc.postgresql.org/)
