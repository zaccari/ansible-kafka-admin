import os
from ansible.module_utils.basic import AnsibleModule, env_fallback


def kafkawrapper(function):
    def wrapper(*args, **kwargs):
        result = {"changed": False, "rc": 0}
        result.update(function(*args, **kwargs))
        return result
    return wrapper


def kafka_argspec():
    argument_spec = dict(
        url=dict(required=False, default=os.environ.get(
            'VAULT_ADDR', ''), type='str'),
        ca_cert=dict(required=False, default=os.environ.get(
            'VAULT_CACERT', ''), type='str'),
        ca_path=dict(required=False, default=os.environ.get(
            'VAULT_CAPATH', ''), type='str'),
        client_cert=dict(required=False, default=os.environ.get(
            'VAULT_CLIENT_CERT', ''), type='str'),
        client_key=dict(required=False, default=os.environ.get(
            'VAULT_CLIENT_KEY', ''), type='str'),
        verify=dict(required=False, default=(
            not os.environ.get('VAULT_SKIP_VERIFY', '')), type='bool'),
        authtype=dict(required=False, default=os.environ.get(
            'VAULT_AUTHTYPE', 'token'), type='str'),
        login_mount_point=dict(required=False, default=os.environ.get(
            'VAULT_LOGIN_MOUNT_POINT', None), type='str'),
        username=dict(required=False, default=os.environ.get(
            'VAULT_USER', ''), type='str'),
        password=dict(required=False, fallback=(
            env_fallback, ['VAULT_PASSWORD']), type='str', no_log=True),
        role_id=dict(required=False, fallback=(env_fallback, [
                     'VAULT_ROLE_ID']), type='str', no_log=True),
        secret_id=dict(required=False, fallback=(
            env_fallback, ['VAULT_SECRET_ID']), type='str', no_log=True),
        aws_header=dict(required=False, fallback=(
            env_fallback, ['VAULT_AWS_HEADER']), type='str', no_log=True),
        namespace=dict(required=False, default=os.environ.get(
            'VAULT_NAMESPACE', None), type='str')
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
