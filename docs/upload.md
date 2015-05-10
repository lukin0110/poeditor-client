Upload to PyPi
==============

Register:
```
python setup.py register -r pypi
```

Upload:
```
python setup.py sdist upload -r pypi
```

Install local:
```
sudo /usr/bin/python setup.py install
```

Make sure on osx to use python 2.7.6 to avoid SSL issues with 2.7.9
