from setuptools import setup

setup( 
    name= 'Check_these_passwords',
    version= '1.0',
    packages= ['Check_these_passwords'],
    entry_points= {
        'console_scripts': [
            'Check_these_passwords = Check_these_passwords.__main__:main'
        ]
    }
)