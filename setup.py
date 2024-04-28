from setuptools import setup

setup( 
    name= 'Check_these_passwords',
    version= '1.0',
    packages= ['folder_to_regroup_files'], # FIXME group the files in a unique directory
    entry_points= {
        'console_scripts': [
            'Check_these_passwords = folder_to_regroup_files.__main__:main' # FIXME pays attention here
        ]
    }
)