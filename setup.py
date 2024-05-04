from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='promethean',
    version='0.1.0',
    description='Run system experiments with ease.',
    long_description=readme,
    author='shg8',
    url='https://github.com/shg8/promethean',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'promethean=promethean.cli:main',
        ],
    },
    install_requires=[
        'pyyaml',
        'jsonschema',
        'paramiko'
    ],
)