#!/usr/bin/env python
from setuptools import setup

py_files = [
    "ansible/module_utils/acl_operation",
    "ansible/module_utils/acl_permission_type",
    "ansible/module_utils/kafka_consumer_lag",
    "ansible/module_utils/kafka_manager",
    "ansible/module_utils/kafka",
    "ansible/module_utils/ssl_utils",
]
files = [
    "ansible/modules/kafka",
]

setup(
    name='ansible-modules-kafka',
    version='0.11.0',
    description='Ansible Modules for Kafka',
    long_description='Ansible Modules for Kafka',
    long_description_content_type='text/x-rst',
    author='Michael Zaccari',
    author_email='michael.zaccari@gmail.com',
    url='https://github.com/zaccari/ansible-kafka-admin',
    py_modules=py_files,
    packages=files,
    install_requires=[
        'ansible>=2.0.0',
        'hvac>=0.9.5',
        'kafka-python>=1.4.5,<2.1.0',
        'kazoo==2.6.1',
        'pure-sasl==0.5.1',
    ],
)
