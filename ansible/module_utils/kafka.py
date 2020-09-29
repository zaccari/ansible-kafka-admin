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
        name=dict(required=True, type='str'),
        bootstrap_servers=dict(required=True, type='list', elements='str'),
        zookeeper=dict(type='str', required=False),
        api_version=dict(required=False, default='2.0.0', type='str'),
        partitions=dict(type='int', required=False, default=1),
        replica_factor=dict(type='int', required=False, default=1),
        state=dict(choices=['present', 'absent'], default='present'),
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
        ssl_context = None
        client = KafkaManager(
            module=module,
            bootstrap_servers=module.params['bootstrap_servers'],
            request_timeout_ms=5000,
            api_version=api_version,
        )
        # ssl_context=params['ssl_context'],
        # sasl_mechanism=sasl_mechanism,
        # sasl_plain_username=sasl_plain_username,
        # sasl_plain_password=sasl_plain_password,
        # sasl_kerberos_service_name=sasl_kerberos_service_name)
    except Exception:
        # e = get_exception()
        # print('Error while initializing Kafka client : %s ' % str(e))
        e = get_exception()
        module.fail_json(
            msg='Error while initializing Kafka client : %s ' % str(e)
        )

    return client
