import settings_handler as sh

def shader_builder(length:int, width, height):
    x1b, x2b = sh.Reference.shader_splitter(sh.Reference.reference_reader(sh.Reference.SCREEN_INITIAL, width, height))
    x3b = x2b
    var = int(sh.Reference.reference_reader(sh.Reference.SCREEN_VARIABLE, width, height))

    x1 = x1b + int(var) * length
    x2 = x2b + int(var) * length
    x3 = x3b + int(var) * length

    effect = '{\\p1}'
    shelter_template = sh.Reference.reference_reader(sh.Reference.SCREEN_TEXT, width, height).format(x1, x2, x3)

    return effect + shelter_template

class ASS_Line(object):
    def __init__(self, start:str, end:str, name:str = None, text:str = None) -> None:
        self.layer = 0
        self.start = start
        self.end = end
        self.style = ''
        self.name = name
        self.margin_set = '0,0,0'
        self.effect = None
        self.text = text

    def build_dialogue(self):
        li = []
        s = ','
        for name, value in vars(self).items():
            if value == None:
                value = ''
            li.append(str(value))
        
        return 'Dialogue: ' + s.join(li)

    def build_comment(self):
        li = []
        s = ','
        for name, value in vars(self).items():
            if value == None:
                value = ''
            li.append(str(value))
        
        return 'Comment: ' + s.join(li)

class Dialogue(ASS_Line):
    def __init__(self, start: str, end: str, name: str = None, text: str = None) -> None:
        super().__init__(start, end, name, text)
        self.layer = 1
        self.style = 'D4DJ 剧情'

class Title(ASS_Line):
    def __init__(self, start: str, end: str, name: str = None, text: str = None) -> None:
        super().__init__(start, end, name, text)
        self.layer = 0
        self.style = 'D4DJ TITLE'

class Shader(ASS_Line):
    def __init__(self, start: str, end: str, name: str = None, text: str = None) -> None:
        super().__init__(start, end, name, text)
        self.layer = 0
        self.style = 'D4DJ shader'

class Caution(ASS_Line):
    def __init__(self, start: str, end: str, name: str = None, text: str = None) -> None:
        super().__init__(start, end, name, text)
        self.layer = 1
        self.style = 'CAUTION'

if __name__ == '__main__':
    pass