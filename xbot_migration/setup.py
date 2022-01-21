from importlib.metadata import entry_points
from setuptools import setup, find_packages

REQUIREMENTS_FILE = "requirements.txt"


def read_requirements(fpath=REQUIREMENTS_FILE):
    with open(fpath) as f:
        requirements = f.readlines()
    return requirements


setup(
    name='xbot-cli',
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'xbot = xbot_migration.xbot:xbot',
        ],
    },
)
