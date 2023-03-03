
# from setuptools import setup, find_packages
# setup(
#     name='goesnex-cli',
#     version='0.1.0',
#     packages=find_packages(),
#     include_package_data=True,
#     package_data={
#     "": [".env"],
#     },
#     py_modules=['main'],
#     install_requires=[
#     'typer',
#     'boto3',
#     'python-dotenv',
#     'pandas',
#     'python-dotenv',
#     'bcrypt'],
#     entry_points='''[console_scripts] 
#     goesnex-cli=main:app
#     ''')


import setuptools

setuptools.setup(
    name="goesnex_cli_package",
    version="0.0.1",
    author="Vikash Singh",
    author_email="singh.vikas@northeastern.edu",
    description="Package to create GOESNEX cli",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
    "": [".env"],
    },
    py_modules=['main'],
    install_requires=[
    'typer',
    'boto3',
    'python-dotenv',
    'pandas',
    'python-dotenv',
    'bcrypt'],
    entry_points='''[console_scripts] 
    goesnex_cli=cli_package.goesnex_cli_package.main:app
    '''
    # python_requires='greaterthan=3.7'
)

