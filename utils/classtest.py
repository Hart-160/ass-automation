class Event(object):

    #event_type = 'Event'

    def __init__(self, index) -> None:
        self.index = index
        self.event_type = 'Event'

    def get_dict(self):
        return {'Index':self.index, 'EventType':self.event_type}

class Dialogue(Event):
    def __init__(self, index, talker, body) -> None:
        super().__init__(index)
        self.event_type = 'Dialogue'
        self.talker = talker
        self.body = body

    def build_body(self):
        str = '\\N'
        return str.join(self.body)

    def get_dict(self):
        return {'Index':self.index, 'EventType':self.event_type, 'Talker':self.talker, 'Body':self.body}

class CloseWindow(Event):
    def __init__(self, index, color = None, fade = None) -> None:
        super().__init__(index)
        self.event_type = 'CloseWindow'
        self.color = color
        self.fade = fade
    
    def get_dict(self):
        if self.color == None:
            return super().get_dict()
        else:
            if self.fade == None:
                return {'Index':self.index, 'EventType':self.event_type, 'Color':self.color}
            else:
                self.fade = float(self.fade)
                return {'Index':self.index, 'EventType':self.event_type, 'Color':self.color, 'Fade':self.fade}

class OpenWindow(Event):
    def __init__(self, index) -> None:
        super().__init__(index)
        self.event_type = 'OpenWindow'

    def get_dict(self):
        return super().get_dict()

class Title(Event):
    def __init__(self, index, body) -> None:
        super().__init__(index)
        self.event_type = 'Title'
        self.body = body

    def get_dict(self):
        return {'Index':self.index, 'EventType':self.event_type, 'Body':self.body}

class Subtitle(Event):
    def __init__(self, index, body) -> None:
        super().__init__(index)
        self.event_type = 'Subtitle'
        self.body = body

    def get_dict(self):
        return {'Index':self.index, 'EventType':self.event_type, 'Body':self.body}

class FontSizeChange(Event):
    def __init__(self, index, font_size) -> None:
        super().__init__(index)
        self.event_type = 'FontSizeChange'
        if font_size == '48':
            self.font_size = 'Default'
        else:
            font_size = int(font_size)
            self.font_size = font_size

    def get_dict(self):
        return {'Index':self.index, 'EventType':self.event_type, 'FontSize':self.font_size}

class Jitter(Event):
    def __init__(self, index, time = None) -> None:
        super().__init__(index)
        self.event_type = 'Jitter'
        self.time = time

    def get_dict(self):
        if self.time == None:
            return super().get_dict()
        else:
            self.time = float(self.time)
            return {'Index':self.index, 'EventType':self.event_type, 'Time':self.time}

