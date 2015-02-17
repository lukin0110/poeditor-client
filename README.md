# poeditor-client

Install the client on your system.

From PyPi:
```
sudo pip install poeditor-client
```

## Example configuration

```
[main]
apikey = 54df54gd5f4gs5df4gsdf54g5sdf4g5dfs4g5dsf4gdsfg

[project.vikingappbe]
project_id = 4200
type = android_strings
trans.en = App/src/main/res/values/strings.xml
trans.nl = App/src/main/res/values-nl/strings.xml
trans.fr = App/src/main/res/values-fr/strings.xml
trans.pl = App/src/poland/res/values-pl/strings.xml
```

## Upload to PyPi

Register:
```
python setup.py register -r pypi
```

Upload:
```
python setup.py sdist upload -r pypi
```


