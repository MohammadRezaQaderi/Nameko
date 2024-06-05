from setuptools import setup, find_packages

setup(
    name='products',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'nameko',
        'nameko-grpc',
    ],
    entry_points={
        'console_scripts': [
            'nameko = nameko.cli:main'
        ]
    }
)
