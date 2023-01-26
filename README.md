# CockroachDB Connectors Performance Testing

## Test Infrastructure

Infrastructure was deployed using Ansible on Google Cloud VMs:

- Single node Confluent Platform (Kafka broker) on a `n2-standard-16` instance type.
- 3 nodes CockroachDB cluster using first the `n2-standard-8` type, and later the `n2-standard-16` instance type.

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

## References

- [Ansible Playbooks for Confluent Platform](https://docs.confluent.io/ansible/current/overview.html)
- [fabiog1901.cockroachdb Ansible Collection](https://github.com/fabiog1901/cockroachdb-collection)
- [JDBC Sink Connector](https://docs.confluent.io/kafka-connectors/jdbc/current/sink-connector/overview.html)
- [Confluent's Python Client confluent-kafka](https://github.com/confluentinc/confluent-kafka-python)
- [PostgreSQL JDBC Driver](https://jdbc.postgresql.org/)
