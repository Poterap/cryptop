from setuptools import setup, find_packages

setup(
    name='cryptop',
    version='0.1.0',
    description='Opis pakietu',
    author='Patryk Potera',
    license='Licencja',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'fastapi',
        'influxdb_client'
    ]
)
