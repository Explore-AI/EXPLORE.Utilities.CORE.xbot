from setuptools import setup, find_packages

setup(
    name='xbot-cli',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='xbot - The EXPLORE Command Line Interface tool for interacting with your data mesh platform',
    long_description=open('README.md').read(),
    install_requires=['requests','argparse','datetime','pytz'],
    url='https://github.com/Explore-AI/EXPLORE.Utilities.CORE.xbot',
    author='EXPLORE-AI CORE Developers',
    author_email='keagan@explore-ai.net'
)