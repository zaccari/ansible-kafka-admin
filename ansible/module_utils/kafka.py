import os
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.pycompat24 import get_exception
from ansible.module_utils.kafka_manager import KafkaManager


def kafkawrapper(function):
    def wrapper(*args, **kwargs):
        result = {"changed": False, "rc": 0}
        result.update(function(*args, **kwargs))
        return result
    return wrapper


def kafka_argspec():
    argument_spec = dict(
        name=dict(type='str', required=True),
        api_version=dict(type='str', required=False, default='2.0.0'),
        partitions=dict(type='int', required=False, default=1),
        replica_factor=dict(type='int', required=False, default=1),
        state=dict(choices=['present', 'absent'], default='present'),
        options=dict(required=False, type='dict', default=None),
        bootstrap_servers=dict(required=False, type='str', default=os.environ.get(
            'KAFKA_BROKERS', '127.0.0.1:9092')),
        zookeeper=dict(type='str', required=False, default=os.environ.get(
            'ZOOKEEPER_SERVERS', '127.0.0.1:2181')),
        zookeeper_sleep_time=dict(type='int', required=False, default=5),
        zookeeper_max_retries=dict(type='int', required=False, default=5),
    )
    return argument_spec


def kafka_init(argument_spec, supports_check_mode=False, required_if=None, required_together=None,
               required_one_of=None, mutually_exclusive=None):
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=supports_check_mode,
                           required_if=required_if, required_together=required_together,
                           required_one_of=required_one_of, mutually_exclusive=mutually_exclusive)
    module.no_log_values.discard("0")
    module.no_log_values.discard(0)
    module.no_log_values.discard("1")
    module.no_log_values.discard(1)
    module.no_log_values.discard(True)
    module.no_log_values.discard(False)
    return module


def kafka_client(module):
    client = None
    api_version = tuple(
        int(p) for p in module.params['api_version'].strip(".").split(".")
    )

    try:
        client = KafkaManager(
            module=module,
            bootstrap_servers=module.params['bootstrap_servers'],
            api_version=api_version,
        )
    except Exception:
        e = get_exception()
        module.fail_json(
            msg='Error while initializing Kafka client : %s ' % str(e)
        )

    return client
