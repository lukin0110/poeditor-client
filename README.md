# poeditor-client
A command line tool which downloads translations from [POEditor](https://poeditor.com) based on a configuration file.

## Install
Install the client on your system. It works on Linux, Mac OS X and Windows. You need to have
[python](https://python.org) and [pip](https://pypi.python.org/pypi/pip) installed.

Install from PyPi:
```
sudo pip install poeditor-client==0.0.2
```

Install pip:
```
sudo easy_install pip
```

## Usage
Run the following command:
```
poeditor_admin.py
```
This will look for a configuration file named `.translations` in the directory where you're executing the command.


## Configuration
Create a file `.translations` in the root of your project.

Example:
```
[main]
apikey = 54df54gd5f4gs5df4gsdf54g5sdf4g5dfs4g5dsf4gdsfg

[project.vikingapp_be]
project_id = 4200
type = android_strings
trans.en = App/src/main/res/values/strings.xml
trans.nl = App/src/main/res/values-nl/strings.xml
trans.fr = App/src/main/res/values-fr/strings.xml
trans.pl = App/src/poland/res/values-pl/strings.xml
```

Parameter       | Description
--------------- | ----------------------------------------------------------------------
apikey          | go to [My Account > API Access](https://poeditor.com/account/api)
project_id      | id of the translation project, can be found under *API Access* as well
type            | type of translation file that you want to download, cfr [export](https://poeditor.com/api_reference/#export)
trans.<locale>  | which language that you want to download and where to store it

## Upload to PyPi

Register:
```
python setup.py register -r pypi
```

Upload:
```
python setup.py sdist upload -r pypi
```


