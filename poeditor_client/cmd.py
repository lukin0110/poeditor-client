import argparse
import os

from ConfigParser import SafeConfigParser
from poeditor import POEditorAPI, POEditorException

FILENAME = ".poeditor"


def _load_config(path):
    """
    Loads the configuration file in the directory that the 'poeditor' cmd is executed.
    """
    if not os.path.exists(path):
        print("Config file '{}' doesn't exist".format(path))
        return None

    parser = SafeConfigParser()
    parser.read(path)
    return parser


def generate():
    """
    Generates an example configuration file.
    """
    parser = SafeConfigParser()
    parser.add_section('main')
    parser.set('main', 'apikey', 'your api key')

    foosection_1 = "project.foo_app_1"
    parser.add_section(foosection_1)
    parser.set(foosection_1, 'project_id', 'your project id')
    parser.set(foosection_1, 'type', 'apple_strings')
    parser.set(foosection_1, 'terms', 'foo_app_1/Localizations/en.lproj/Localizable.strings')
    parser.set(foosection_1, 'trans.en', 'foo_app_1/Localizations/en.lproj/Localizable.strings')
    parser.set(foosection_1, 'trans.nl', 'foo_app_1/Localizations/nl.lproj/Localizable.strings')
    parser.set(foosection_1, 'trans.fr', 'foo_app_1/Localizations/fr.lproj/Localizable.strings')

    foosection_2 = "project.foo_app_2"
    parser.add_section(foosection_2)
    parser.set(foosection_2, 'project_id', 'your project id')
    parser.set(foosection_2, 'type', 'apple_strings')
    parser.set(foosection_2, 'trans.pl', 'foo_app_2/Localizations/pl.lproj/Localizable.strings')

    parser.write(open(FILENAME, "w+"))


def init(config):
    """
    Initializes the project on POEditor based on the configuration file.
    """
    assert config
    client = POEditorAPI(api_token=config.get("main", "apikey"))
    sections = config.sections()

    for s in sections:
        if s.startswith("project."):
            print(" - Project: {}".format(s))
            project_id = config.get(s, "project_id")

            # 1. Push terms
            terms = config.get(s, 'terms', None) if config.has_option(s, 'terms') else None
            if terms:
                project_id = config.get(s, "project_id")
                print(" - Terms: {0}".format(terms))
                client.update_terms(project_id, terms)

            # 2. Create/add languages
            options = config.options(s)
            for o in options:
                if o.startswith("trans."):
                    lang = o[6:]

                    try:
                        client.add_language_to_project(project_id, lang)
                    except POEditorException:
                        pass

                    client.update_definitions(
                        project_id=project_id,
                        file_path=config.get(s, o),
                        language_code=lang,
                        overwrite=True
                    )
                    print(" - Language added: {}".format(lang))


def pull(config):
    """
    Pulls translations from the POEditor API.
    """
    assert config
    client = POEditorAPI(api_token=config.get("main", "apikey"))
    sections = config.sections()

    for s in sections:
        if s.startswith("project."):
            print("\nProject: {}".format(s))
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
                    print("Language: {}".format(language))
                    client.export(project_id, language_code=language, file_type=file_type, local_file=export_path)


def pushTerms(config):
    """
    Pushes new terms to POEditor
    """
    assert config
    client = POEditorAPI(api_token=config.get("main", "apikey"))
    sections = config.sections()

    for s in sections:
        if s.startswith("project."):
            terms = config.get(s, 'terms', None) if config.has_option(s, 'terms') else None
            if terms:
                project_id = config.get(s, "project_id")
                print(" - Project: {0}, {1}\n".format(s, terms))
                client.update_terms(project_id, terms)


def main():
    """
    ./test.py init -f examples/.poeditor0
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', '-f', default=FILENAME)
    parser.add_argument('command', choices=('init', 'generate', 'pull', 'pushTerms'))

    args = parser.parse_args()
    config = _load_config(args.config_file)

    if "init" == args.command:
        print("Initialize project")
        init(config)

    if 'generate' == args.command:
        print("Generate configuration file")
        generate()

    elif "pull" == args.command:
        print("Download translations")
        pull(config)

    elif "pushTerms" == args.command:
        print("Push terms")
        pushTerms(config)
