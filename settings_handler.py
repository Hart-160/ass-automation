import os

'''
这个部分负责读取设置文件供视频分析及字幕写入使用
'''

class AutoRead(object):
    def auto_settings(param, width, height) -> str:
        if param == '[Sample ASS Path]':
            res = AutoRead.get_preferred_ass(width, height)
            return res
        if param == '[Default Reference Path]':
            res = AutoRead.get_preferred_ref(width, height)
            return res

    def __split_res(name):
        pos = name.find(']')
        name = name[1:pos]
        wid, hei = name.split('x')
        return int(wid), int(hei)

    def get_preferred_ref(width, height) -> str:
        refs = []
        li = os.listdir(os.getcwd())
        for l in li:
            if '[' in l and ']reference.txt' in l:
                refs.append(l)

        for r in refs:
            r_width, r_height = AutoRead.__split_res(r)
            if int(r_width) == width and int(r_height) == height:
                return r

    def get_preferred_ass(width, height):
        refs = []
        li = os.listdir(os.getcwd())
        for l in li:
            if '[' in l and ']untitled.ass' in l:
                refs.append(l)

        for r in refs:
            r_width, r_height = AutoRead.__split_res(r)
            if int(r_width) == width and int(r_height) == height:
                return r
class Settings(object):
    SAMPLE_ASS_PATH = '[Sample ASS Path]'
    DEFAULT_REFERENCE_PATH = '[Default Reference Path]'
    DEFAULT_LOWER_RANGE = '[Default Lower Range]'
    DEFAULT_UPPER_RANGE = '[Default Upper Range]'
    OPEN_BOX_OFFSET = '[Open Box Offset]'
    NORMAL_CLOSE_OFFSET = '[Normal Close Offset]'
    BLACK_FADEIN_OFFSET = '[Black Fade-in Offset]'

    def settings_reader(parameter, width = None, height = None) ->str:
        with open('settings.txt', 'r', encoding='utf-8') as f:
            li = f.readlines()

        for i in range(len(li)):
            if parameter in li[i]:
                res = li[i+1].replace('\n', '')
                if res == 'automatic':
                    res = AutoRead.auto_settings(parameter, width, height)
                    return res
                else:
                    return res

    def hsv_range_splitter(line):
        li = line.split()
        h = li[0]
        s = li[1]
        v = li[2]
        return int(h), int(s), int(v)

class Reference(object):
    SCREEN_TEXT = '[SCREEN TEXT]'
    SCREEN_INITIAL = '[SCREEN INITIAL]'
    SCREEN_VARIABLE = '[SCREEN VARIABLE]'
    TEXT_WORD_MX = '[TEXT WORD MX]'
    TEXT_BORDER_MX = '[TEXT BORDER MX]'

    def reference_reader(parameter, width = None, height = None) ->str:
        route = Settings.settings_reader(Settings.DEFAULT_REFERENCE_PATH, width, height)
        with open(route, 'r', encoding='utf-8') as f:
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
    pass