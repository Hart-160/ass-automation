class Settings(object):
    SAMPLE_ASS_PATH = '[Sample ASS Path]'
    DEFAULT_REFERENCE_PATH = '[Default Reference Path]'
    OPEN_BOX_OFFSET = '[Open Box Offset]'
    NORMAL_CLOSE_OFFSET = '[Normal Close Offset]'
    BLACK_FADEIN_OFFSET = '[Black Fade-in Offset]'

    def settings_reader(parameter):
        with open('settings.txt', 'r', encoding='utf-8') as f:
            li = f.readlines()

        for i in range(len(li)):
            if parameter in li[i]:
                res = li[i+1].replace('\n', '')
                return res

class Reference(object):
    SCREEN_TEXT = '[SCREEN TEXT]'
    SCREEN_INITIAL = '[SCREEN INITIAL]'
    TEXT_WORD_MX = '[TEXT WORD MX]'
    TEXT_BORDER_MX = '[TEXT BORDER MX]'

    def reference_reader(parameter):
        with open(Settings.settings_reader(Settings.DEFAULT_REFERENCE_PATH), 'r', encoding='utf-8') as f:
            li = f.readlines()

        for i in range(len(li)):
            if parameter in li[i]:
                res = li[i+1].replace('\n', '')
                return res

    def shader_splitter(line):
        li = line.split()
        x1 = li[0]
        x2 = li[1]
        return int(x1), int(x2)

    def box_splitter(line):
        li = line.split()
        x1 = li[0]
        y1 = li[1]
        x2 = li[2]
        y2 = li[3]
        return int(x1), int(y1), int(x2), int(y2)

if __name__ == '__main__':
    #print(Settings.settings_reader(Settings.DEFAULT_REFERENCE_PATH))
    print(Settings.settings_reader(Settings.SAMPLE_ASS_PATH))