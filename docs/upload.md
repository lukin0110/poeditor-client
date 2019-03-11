Upload to PyPi
==============

Register:
```
python setup.py register -r pypi
```

Upload:
```
sudo /usr/bin/python setup.py sdist upload -r pypi
```

Install local:
```
sudo /usr/bin/python setup.py install
```

Make sure on osx to use python 2.7.6 to avoid SSL issues with 2.7.9

Using Docker
------------
```bash
$ docker-compose build
$ docker-compose run app upload
```

Docs
----
* http://peterdowns.com/posts/first-time-with-pypi.html
