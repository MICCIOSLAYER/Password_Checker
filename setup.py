from setuptools import setup, find_packages

setup(
    name='Password_Checker',
    version='0.1.0',
    requires=['requests==2.30', 'hashlib', 'sys', 'os', 're', 'argparse',
              'response', 'pathlib', 'getpass', 'logging', 'configparser'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Check-these-passwords = Password_Checker.__main__:main'
        ]
    },
    url='https://github.com/MICCIOSLAYER/Password_Checker.git',
    author='Renato Eliasy',
    author_email='renatoeliasy@gmail.com',
    license='MIT'
)
