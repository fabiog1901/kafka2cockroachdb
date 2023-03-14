#!/usr/bin/python

from ansible_runner import Runner, RunnerConfig
import yaml
import os
import sys
import time

pwd = os.getcwd()

skip_tags = ','.join(sys.argv[1:])

# load Ansible "extra-vars"
with open('kafka2crdb.vars.yaml', 'r') as f:
    ev = yaml.safe_load(f)


ev['deployment_id'] = 'k2crdb'

# First, provision the Kafka cluster
# the playbook saves the inventory in file 'k2crdb.ini'
rc = RunnerConfig(
    private_data_dir=pwd,
    playbook="kafka.yaml",
    extravars=ev,
    skip_tags=skip_tags
)

rc.prepare()
r = Runner(config=rc)
r.run()

# loop through various cpu sizes for the crdb nodes
for x in ev['cluster_cpus']:

    ev['deployment_id'] = f'k2crdb{x}'

    ev['vcpus'] = x

    # create a CockroachDB cluster with x vcpus nodes
    rc = RunnerConfig(
        private_data_dir=pwd,
        playbook="cockroachdb.yaml",
        extravars=ev,
        inventory='k2crdb.ini',
        skip_tags=skip_tags
    )

    rc.prepare()
    r1 = Runner(config=rc)
    r1.run()

    # cycle through all partitions and batch sizes
    for p in ev['k_partitions']:

        ev['kp'] = p

        rc = RunnerConfig(
            private_data_dir=pwd,
            playbook="kafka-producer.yaml",
            extravars=ev,
            inventory=f'k2crdb{x}.ini',
            skip_tags=skip_tags
        )

        rc.prepare()

        r2 = Runner(config=rc)
        r2.run()

        for b in ev['batch_sizes']:

            ev['batch_size'] = b

            rc = RunnerConfig(
                private_data_dir=pwd,
                playbook="kafka-consumer.yaml",
                extravars=ev,
                inventory=f'k2crdb{x}.ini',
                skip_tags=skip_tags
            )

            rc.prepare()

            r3 = Runner(config=rc)
            r3.run()

        # stop the producer and pause 10 mins between partition test runs
        rc = RunnerConfig(
            private_data_dir=pwd,
            playbook="kafka-producer.yaml",
            extravars=ev,
            inventory=f'k2crdb{x}.ini',
            skip_tags="provision-topic,gen-data"
        )

        rc.prepare()

        r4 = Runner(config=rc)
        r4.run()
        
        print("\npause 10 minutes between partition test runs....\n")
        time.sleep(600)


    # fetching stats and tsdump
    rc = RunnerConfig(
        private_data_dir=pwd,
        playbook="collect-stats.yaml",
        extravars=ev,
        inventory='k2crdb.ini',
        skip_tags='local_stats'
    )

    rc.prepare()
    r7 = Runner(config=rc)
    r7.run()
    