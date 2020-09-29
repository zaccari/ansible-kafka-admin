#!/usr/bin/env python

from pkg_resources import parse_version
from ansible.module_utils.pycompat24 import get_exception
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
    kafka_topic(module)


@kafkawrapper
def kafka_topic(module):
    name = module.params['name']
    partitions = module.params['partitions']
    replica_factor = module.params['replica_factor']
    state = module.params['state']
    zookeeper = module.params['zookeeper']
    zookeeper_sleep_time = module.params['zookeeper_sleep_time']
    zookeeper_max_retries = module.params['zookeeper_max_retries']
    options = []
    if module.params['options'] is not None:
        options = module.params['options'].items()

    changed = False
    client = kafka_client(module)

    msg = 'Topic \'%s\': ' % (name)

    if state == 'present':
        if name in client.get_topics():
            # Topic exists
            if zookeeper == '':
                module.fail_json(
                    msg='\'zookeeper\', parameter is needed when '
                    'parameter \'state\' is \'present\' for resource '
                    '\'topic\'.'
                )

            try:
                client.init_zk_client(hosts=zookeeper)
            except Exception:
                e = get_exception()
                module.fail_json(
                    msg='Error while initializing Zookeeper client : '
                    '%s. Is your Zookeeper server available and '
                    'running on \'%s\'?' % (str(e), zookeeper)
                )

            if client.is_topic_configuration_need_update(name,
                                                         options):
                if not module.check_mode:
                    client.update_topic_configuration(name, options)
                changed = True

            if partitions > 0 and replica_factor > 0:
                # partitions and replica_factor are set
                if client.is_topic_replication_need_update(
                        name, replica_factor
                ):
                    json_assignment = (
                        client.get_assignment_for_replica_factor_update(
                            name, replica_factor
                        )
                    )
                    if not module.check_mode:
                        client.update_admin_assignment(
                            json_assignment,
                            zookeeper_sleep_time,
                            zookeeper_max_retries
                        )
                    changed = True

                if client.is_topic_partitions_need_update(
                        name, partitions
                ):
                    cur_version = parse_version(client.get_api_version())
                    if not module.check_mode:
                        if cur_version < parse_version('1.0.0'):
                            json_assignment = (
                                client.get_assignment_for_partition_update
                                (name, partitions)
                            )
                            zknode = '/brokers/topics/%s' % name
                            client.update_topic_assignment(
                                json_assignment,
                                zknode
                            )
                        else:
                            client.update_topic_partitions(name,
                                                           partitions)
                    changed = True
                client.close_zk_client()
                if changed:
                    msg += 'successfully updated.'
            else:
                # 0 or "default" (-1)
                module.warn(
                    "Current values of 'partitions' (%s) and "
                    "'replica_factor' (%s) does not let this lib to "
                    "perform any action related to partitions and "
                    "replication. SKIPPING." % (partitions, replica_factor)
                )

        else:
            # Create topic
            if not module.check_mode:
                client.create_topic(
                    module.params['name'],
                    module.params['partitions'],
                    module.params['replica_factor'],
                    config_entries=module.params['options'].items(),
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

    client.close()

    if not changed:
        msg += 'nothing to do.'

    module.exit_json(changed=changed, msg=msg)


if __name__ == '__main__':
    main()
