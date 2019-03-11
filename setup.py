from setuptools import setup, find_packages


long_description = """
The POEditor Client is a command line tool that enables you to easily manage your translation files within a project.
"""

import poeditor_client

setup(
    name="poeditor_client",
    version=poeditor_client.__version__,
    url='https://github.com/lukin0110/poeditor-client',
    license='LICENSE.txt',
    description='The POEditor Client',
    scripts=[
        'scripts/poeditor',
    ],
    author='Maarten Huijsmans',
    author_email='maarten@lukin.be',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    long_description=long_description,
    python_requires='>3.6.0',
    install_requires=[
       "poeditor==1.1.0",
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Shells',
    ],
)
