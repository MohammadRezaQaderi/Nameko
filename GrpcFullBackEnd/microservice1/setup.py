from setuptools import setup, find_packages

setup(
    name='microservice1',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'nameko==3.0.0rc9',
        'sqlalchemy==1.4.18',
        'psycopg2-binary==2.9.1',
        'redis==3.5.3'
    ],
)
