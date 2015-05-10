import argparse
import os
import sys

from ConfigParser import SafeConfigParser, ConfigParser, DEFAULTSECT
from poeditor import POEditorAPI

FILENAME = ".poeditor"

#TODO: push terms, init, readme file, pypi, create exe

def _load_config():
    """
    Loads the configuration file in the directory that the 'poeditor' cmd is executed.
    """
    config_file = os.path.join('.', FILENAME)
    parser = SafeConfigParser()
    parser.read(config_file)
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
    parser.set(foosection_1, 'trans.en', 'foo_app_1/Localizations/BE/en.lproj/Localizable.strings')
    parser.set(foosection_1, 'trans.nl', 'foo_app_1/Localizations/BE/nl.lproj/Localizable.strings')
    parser.set(foosection_1, 'trans.fr', 'foo_app_1/Localizations/BE/fr.lproj/Localizable.strings')

    foosection_2 = "project.foo_app_2"
    parser.add_section(foosection_2)
    parser.set(foosection_2, 'project_id', 'your project id')
    parser.set(foosection_2, 'type', 'apple_strings')
    parser.set(foosection_2, 'trans.pl', 'foo_app_2/Localizations/PL/pl.lproj/Localizable.strings')

    parser.write(open(FILENAME, "w+"))


def init(config):
    """
    Initializes the project on POEditor based on the configuration file.
    """
    """
    public class InitTask extends BaseTask {

        @Override
        public void handle() {
            System.out.println("Initializing");
            Project details = client.getProject(config.getProjectId());

            if(details != null){
                Path current = Paths.get("");

                // Uploading terms
                if(config.getTerms() != null) {
                    File termsFile = new File(current.toAbsolutePath().toString(), config.getTerms());
                    UploadDetails ud = client.uploadTerms(config.getProjectId(), termsFile);
                    System.out.println("- terms uploaded: " + ud);
                } else {
                    System.out.println("- no terms defined");
                }

                // Create languages
                for(String lang : config.getLanguageKeys()){
                    client.addProjectLanguage(config.getProjectId(), lang);
                    System.out.println("- lang added: " + lang);
                    File langFile = new File(current.toAbsolutePath().toString(), config.getLanguage(lang));
                    client.uploadLanguage(config.getProjectId(), langFile, lang, true);
                    System.out.println("- lang uploaded: " + lang);
                }
            } else {
                System.out.println("Project with id '" + config.getProjectId() + "' doesn't exist.");
            }
        }
    }
    """
    pass


def pull(config):
    """
    Pulls translations from the POEditor API.
    """
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


def pushTerms(config):
    """
    Pushes new terms to POEditor
    """
    """
    public class PushTermsTask extends BaseTask {

        @Override
        public void handle() {
            System.out.println("Pushing terms");

            if(config.getTerms() != null) {
                Path current = Paths.get("");
                File termsFile = new File(current.toAbsolutePath().toString(), config.getTerms());
                UploadDetails details = client.uploadTerms(config.getProjectId(), termsFile, config.getTagsAll(), config.getTagsNew(), config.getTagsObsolete());
                System.out.println("Synced: " + details);
            } else {
                System.out.println("No terms defined");
            }
        }
    }
    """
    pass


def main():
    cmd = sys.argv[1]
    #print "Cmd: ", cmd

    if 'generate' == cmd:
        print "Generate configuration file"
        generate()

    elif "init" == cmd:
        print "Initialize project"
        init(_load_config())

    elif "pull" == cmd:
        print "Download translations"
        pull(_load_config())

    elif "pushTerms" == cmd:
        print "Push terms"
        pushTerms(_load_config())
