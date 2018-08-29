import argparse
import os
from time import sleep

from ConfigParser import NoOptionError, NoSectionError, SafeConfigParser
from poeditor import POEditorAPI, POEditorException

FILENAME = ".poeditor"


def _get_api_token(config):
    """
    Get the API key either from the config file or the environment variables.
    """
    assert config
    try:
        return config.get("main", "apikey")
    except (NoOptionError, NoSectionError):
        return os.environ.get('POEDITOR_TOKEN')


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
    client = POEditorAPI(api_token=_get_api_token(config))
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


def pull(config, languages=None):
    """
    Pulls translations from the POEditor API.
    """
    assert config
    client = POEditorAPI(api_token=_get_api_token(config))
    sections = config.sections()

    for s in sections:
        if s.startswith("project."):
            print("\nProject: {}".format(s))
            project_id = config.get(s, "project_id")
            file_type = config.get(s, "type")
            options = config.options(s)

            for o in options:
                if o.startswith("trans."):
                    language = o[6:]
                    if languages and language not in languages:
                        continue

                    export_path = config.get(s, o)
                    parent_dir = os.path.dirname(export_path)
                    if not os.path.exists(parent_dir):
                        os.makedirs(parent_dir)

                    print("Language: {}".format(language))
                    client.export(project_id, language_code=language, file_type=file_type, local_file=export_path)


def push(config, languages=None, overwrite=False, sync_terms=False):
    """
    Push terms and languages
    """
    assert config
    client = POEditorAPI(api_token=_get_api_token(config))
    sections = config.sections()

    for section in sections:
        if not section.startswith("project."):
            continue

        print("Project: {}".format(section))
        project_id = config.get(section, "project_id")
        options = config.options(section)

        for option in options:
            if option.startswith("trans."):
                import_path = config.get(section, option)
                language = option.split('.', 1)[-1]
                if languages and language not in languages:
                    continue

                if not os.path.exists(import_path):
                    print("Error: {path} doesn't exist: ignoring language '{language}'"
                          .format(path=import_path, language=language))
                    continue

                print("    Pushing language '{}'...".format(language))
                client.update_terms_definitions(
                    project_id,
                    language_code=language,
                    file_path=import_path,
                    overwrite=overwrite,
                    sync_terms=sync_terms
                )
                sleep(10.5)  # Avoids API rate limit


def pushTerms(config, sync_terms=False):
    """
    Pushes new terms to POEditor
    """
    assert config
    client = POEditorAPI(api_token=_get_api_token(config))
    sections = config.sections()

    for s in sections:
        if s.startswith("project."):
            terms = config.get(s, 'terms', None) if config.has_option(s, 'terms') else None
            if terms:
                project_id = config.get(s, "project_id")
                print(" - Project: {0}, {1}\n".format(s, terms))
                client.update_terms(project_id, terms, sync_terms=sync_terms)
                sleep(10.5)  # Avoids API rate limit


def status(config):
    """
    Status is a simple task that displays the existing project configuration in a more human readable format.
    It lists all resources that have been initialized under the local project and all their associated translation
    files.
    """
    assert config
    client = POEditorAPI(api_token=_get_api_token(config))
    sections = config.sections()

    print("Api key: {}".format(config.get("main", "apikey")))

    for s in sections:
        if s.startswith("project."):
            project_id = config.get(s, "project_id")
            details = client.view_project_details(project_id)
            terms = config.get(s, 'terms', None) if config.has_option(s, 'terms') else None
            options = config.options(s)

            print("\nProject: {0} ({1})".format(details['name'], details['id']))
            print("Terms: {0}".format(terms))

            for option in options:
                if option.startswith("trans."):
                    import_path = config.get(s, option)
                    language = option.split('.', 1)[-1]
                    print(" - Language {0}: {1}".format(language, import_path))


def main():
    """
    ./test.py init -f examples/.poeditor0
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', '-f', default=FILENAME)
    parser.add_argument('--overwrite', default=False, action="store_true",
                        help="Overwrites definitions when pushing a file.")
    parser.add_argument('--sync-terms', default=False, action="store_true",
                        help="Syncing terms deletes terms that are not found in the pushed file and adds new ones.")
    parser.add_argument('command', choices=('init', 'generate', 'pull', 'push', 'pushTerms', 'status'))
    parser.add_argument('languages', default=None, nargs="*")

    args = parser.parse_args()
    config = _load_config(args.config_file)
    languages = args.languages[1:] if args.languages else None

    if "init" == args.command:
        print("Initialize project")
        init(config)

    if 'generate' == args.command:
        print("Generate example configuration file")
        generate()

    elif "pull" == args.command:
        print("Download translations")
        pull(config, languages=languages)

    elif "push" == args.command:
        print("Push languages")
        push(config, languages=languages, overwrite=args.overwrite, sync_terms=args.sync_terms)

    elif "pushTerms" == args.command:
        print("Push terms")
        pushTerms(config, sync_terms=args.sync_terms)

    elif "status" == args.command:
        status(config)
