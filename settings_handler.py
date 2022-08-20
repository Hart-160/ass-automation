import os

class Settings(object):
    SAMPLE_ASS_PATH = '[Sample ASS Path]'
    DEFAULT_REFERENCE_PATH = '[Default Reference Path]'

    def settings_reader(parameter):
        with open('settings.txt', 'r', encoding='utf-8') as f:
            li = f.readlines()

        for i in range(len(li)):
            if parameter in li[i]:
                return li[i+1]

class Reference(object):
    SCREEN_TEXT = '[SCREEN TEXT]'
    SCREEN_INITIAL = '[SCREEN INITIAL]'
    SCREEN_VARIABLE = '[SCREEN VARIABLE]'
    TEXT_WORD_MX = '[TEXT WORD MX]'
    TEXT_BORDER_MX = '[TEXT BORDER MX]'

    def reference_reader(parameter):
        with open(Settings.settings_reader(Settings.DEFAULT_REFERENCE_PATH), 'r', encoding='utf-8') as f:
            li = f.readlines()

        for i in range(len(li)):
            if parameter in li[i]:
                return li[i+1]

if __name__ == '__main__':
    print(Settings.settings_reader(Settings.DEFAULT_REFERENCE_PATH))
    print(Reference.reference_reader(Reference.SCREEN_TEXT))