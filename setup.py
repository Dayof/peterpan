from setuptools import setup

setup(
    name='peterpan',
    version='1.0',
    long_description=__doc__,
    packages=['peterpan'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask',
                    'beautifulsoup4']
)
