#!/usr/bin/python
# -*- encoding: utf-8 -*-
# POEditor Client: https://github.com/sporteasy/python-poeditor/
# Fork: https://github.com/lukin0110/python-poeditor
import os

from ConfigParser import SafeConfigParser, ConfigParser, DEFAULTSECT
from poeditor import POEditorAPI

FILENAME = ".translations"


def load_config():
    config_file = os.path.join('.', FILENAME)
    parser = SafeConfigParser()
    parser.read(config_file)
    return parser


def download(config):
    client = POEditorAPI(api_token=config.get("main", "apikey"))
    sections = config.sections()

    for s in sections:
        if s.startswith("project."):
            print "\nProject: ", s
            project_id = config.get(s, "project_id")
            file_type = config.get(s, "type")
            options = config.options(s)

            for o in options:
                if o.startswith("trans."):
                    export_path = config.get(s, o)
                    parent_dir = os.path.dirname(export_path)
                    if not os.path.exists(parent_dir):
                        os.makedirs(parent_dir)
                    language = o[6:]
                    print "Language: ", language
                    client.export(project_id, language_code=language, file_type=file_type, local_file=export_path)


if __name__ == "__main__":
    config = load_config()
    download(config)
    #print "\nSections: ", config.sections()
    print "\nDone!"
