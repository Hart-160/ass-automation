import os

class Settings(object):
    def __init__(self) -> None:
        with open('settings.txt', 'r', encoding='utf-8') as setting:
            self.li = setting.readlines()

    def settings_reader(self, parameter):
        for i in range(len(self.li)):
            if parameter in self.li[i]:
                return self.li[i+1]

class Reference(object):
    def __init__(self) -> None:
        pass

if __name__ == '__main__':
    pass