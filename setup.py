from setuptools import setup

setup(
    name="poeditor-client",
    version="0.0.1",
    url='https://github.com/lukin0110/poeditor-client',
    license='LICENSE.txt',
    description='Download translation files from POEditor',
    scripts=[
        'scripts/poeditor_admin.py'
    ],
    author='Maarten Huijsmans',
    author_email='maarten@lukin.be',
    install_requires=[
        "poeditor==1.0.3",
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
