def shader_builder(length:int):
    x1b = 495
    x2b = x3b = 512
    var = 46

    x1 = x1b + var * length
    x2 = x2b + var * length
    x3 = x3b + var * length

    effect = '{\\p1}'
    shelter_template = 'm 242 1182 l {0} 1182 {1} 1164 {2} 1149 1683 1149 1688 1150 1691 1151 1698 1159 1700 1165 1700 1182 1700 1330 1699 1334 1697 1338 1694 1342 1647 1389 1639 1391 244 1391 230 1389 224 1384 222 1379 220 1376 220 1209 222 1203 224 1200'.format(x1, x2, x3)
    #0char: 496, 513, 513 (+44 per char)

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