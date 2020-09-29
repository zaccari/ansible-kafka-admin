#!/usr/bin/env python

from ansible.module_utils.kafka import kafkawrapper
from ansible.module_utils.kafka import kafka_argspec
from ansible.module_utils.kafka import kafka_init
from ansible.module_utils.kafka import kafka_client
from pprint import pprint
import json

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community', 'version': '1.1'}
DOCUMENTATION = '''
---
module: kafka_topic
version_added: "1.2.0"
short_description: Kafka topic management
description:
    - Module to manage Kafka topics
extends_documentation_fragment: kafka
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - kafka_topic:
        name: test
        bootstrap_servers: 127.0.0.1:9092
'''


def main():
    argspec = kafka_argspec()
    module = kafka_init(argspec)
    result = kafka_topic(module)

    # if result.get('failed'):
    #     module.fail_json(**result)
    # else:
    #     module.exit_json(**result)


@kafkawrapper
def kafka_topic(module):
    name = module.params['name']
    state = module.params['state']
    changed = False
    client = kafka_client(module)

    msg = 'Topic \'%s\': ' % (name)

    if state == 'present':
        if name in client.get_topics():
            # Topic exists
            print("Do nothing")
        else:
            # Create topic
            if not module.check_mode:
                client.create_topic(
                    module.params['name'],
                    module.params['partitions'],
                    module.params['replica_factor'],
                )
            changed = True
            msg += 'successfully created.'

    elif state == 'absent':
        if name in client.get_topics():
            # delete topic
            if not module.check_mode:
                client.delete_topic(name)
            changed = True
            msg += 'successfully deleted.'

        # client.create_topic(
        #     module.params['name'],
        #     module.params['partitions'],
        #     module.params['replica_factor'],
        # )
    client.close()

    if not changed:
        msg += 'nothing to do.'

    module.exit_json(changed=changed, msg=msg)


def create_topic(client, params):
    client.create_topic(
        module.params['name'],
        module.params['partitions'],
        module.params['replica_factor'],
    )


if __name__ == '__main__':
    main()
