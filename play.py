#!/usr/bin/python

from ansible_runner import Runner, RunnerConfig
import yaml
import os
import sys

pwd = os.getcwd()

# First, provision the Kafka cluster
skip_tags = ','.join(sys.argv[1:])


with open('kafka2crdb.vars.yaml', 'r') as f:
    ev = yaml.safe_load(f)


ev['deployment_id'] = 'k2crdb'

rc = RunnerConfig(
    private_data_dir=pwd,
    playbook="kafka.yaml",
    extravars=ev,
    verbosity=1,  
    skip_tags=skip_tags
    )

rc.prepare()
r = Runner(config=rc)
r.run()

# loop through various cpu sizes for the crdb nodes
for x in ev['cluster_cpus']:
    
    ev['deployment_id'] = f'k2crdb{x}'
    
    ev['vcpus'] = x
       
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
    

    

