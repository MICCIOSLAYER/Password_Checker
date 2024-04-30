from setuptools import setup, find_packages

setup( 
    name= 'Password_Checker',
    version= '0.1.0',
    packages= find_packages(),
    entry_points= {
        'console_scripts': [
            'Check_this = Check_these_passwords.__main__:main' 
        ]
    },
    url='https://github.com/MICCIOSLAYER/Password_Checker.git',
    author='Renato Eliasy',
    author_email='renatoeliasy@gmail.com',
    license='MIT'
)