poeditor-client
===============
[![Build Status](https://travis-ci.org/lukin0110/poeditor-client.svg)](https://travis-ci.org/lukin0110/poeditor-client)

A command line tool which downloads translations from [POEditor](https://poeditor.com) based on a configuration file.

1. Install
----------
Install the client on your system. It works on Linux, Mac OS X and Windows. You need to have
[python](https://python.org) and [pip](https://pypi.python.org/pypi/pip) installed.

Install from PyPi:
```
sudo pip install poeditor-client==0.0.6
```

Install pip:
```
sudo easy_install pip
```

2. Configuration
----------------
Create a file `.poeditor` in the root of your project.


**Note:** For security reasons it's recommended that you use the `POEDITOR_TOKEN` 
environment variables to store you API key:
```
export POEDITOR_TOKEN=54df54gd5f4gs5sdfsdfsdfasdfsdfasdfasdf
```

**Example:**
```
[main]
apikey = 54df54gd5f4gs5sdfsdfsdfasdfsdfasdfasdf; **Note:** Use the POEDITOR_TOKEN instead

[project.vikingapp_be]
project_id = 4200
type = android_strings
terms = App/src/main/res/values/strings.xml
trans.en = App/src/main/res/values/strings.xml
trans.nl = App/src/main/res/values-nl/strings.xml
trans.fr = App/src/main/res/values-fr/strings.xml

[project.cat_pictures]
project_id = 4201
type = json
terms = App/src/main/res/values/strings.json
trans.en = App/src/main/res/values/strings.json
trans.nl = App/src/main/res/values-nl/strings.json
trans.fr = App/src/main/res/values-fr/strings.json
```


Parameter                                         | Description
------------------------------------------------- | ----------------------------------------------------------------------
apikey (or `POEDITOR_TOKEN` environment variable) | go to [My Account > API Access](https://poeditor.com/account/api)
project_id                                        | id of the translation project, can be found under *API Access* as well
type                                              | file format  (po, pot, mo, xls, apple_strings, xliff, android_strings, resx, resw, properties, json) , cfr [export](https://poeditor.com/api_reference/#export)
trans.*locale*                                    | which language that you want to download and where to store it

3. Usage
--------
After your have created your translation project on POEditor you can can initialize your project based on your
configuration. The cmd will load the `.poeditor` file in the directory where you're executing the command.

Initialize:
```
poeditor init
```
This will create terms and add languages to your project.


Download translations:
```
poeditor pull
```

Upload languages:
```
poeditor push
```

Add terms:
```
poeditor pushTerms
```

Check project status:
```
poeditor status
```

License
=======

    Copyright 2015 Maarten Huijsmans

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
