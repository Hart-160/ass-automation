import generate_tmp as gt

'''
这个部分负责从sce提取出可供视频分析校验的列表
'''

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

class DialogueSections:
    def __clean_text(text:str) -> str:
        li = text.split('＠')
        res = li[0]
        return res

    def sce_handler(route) -> list:
        '''
        输入sce路径，输出一个包含各节点的列表
        '''
        lis = []
        with open(route, 'r+', encoding='utf-8') as s:
            li = s.readlines()

        for l in li:
            if l == '\n':
                continue
            elif gt.SCEwords.background_name in l:
                continue
            elif gt.SCEwords.live2d_disappear in l:
                continue
            if gt.SCEwords.live2d_film in l:
                continue
            else:
                lis.append(l)

        event_list = []
        index = 1
        search = 10
        talker = ''

        for i in range(len(lis)):
            line = lis[i]
            line = line.replace('\u3000', '')

            if 'タイトル' in line and line.startswith(gt.SCEwords.start):
                #判断标题和副标题
                slic = line.find('：')
                temp = line.replace(gt.SCEwords.end, '')
                body = temp[slic + 1:]
                if gt.SCEwords.title in line:
                    tit = Title(index, body)
                else:
                    tit = Subtitle(index, body)
                event_list.append(tit.get_dict())

            elif gt.SCEwords.close_window in line:
                # 判断对话框消失
                if gt.SCEwords.fade_in in lis[i-1]:
                    # 带有颜色变化的对话框消失
                    cw = CloseWindow(index - 1, 'CloseWindow')
                    temp = lis[i-1].replace(gt.SCEwords.fade_in, '')
                    color = temp[0]
                    cw.color = color
                    if gt.SCEwords.fade_time in lis[i-1]:
                        temp1 = lis[i-1].find(gt.SCEwords.fade_time)
                        temp2 = lis[i-1].find(gt.SCEwords.end_backup, temp1)
                        temp = lis[i-1][temp1:temp2]
                        fade = temp.split('：')[1]
                        cw.fade = fade
                else:
                    # 普通的对话框消失
                    cw = CloseWindow(index - 1)
                if event_list[-1]['EventType'] == 'CloseWindow':
                    continue
                event_list.append(cw.get_dict())

            elif gt.SCEwords.open_window in line:
                # 判断对话框弹出
                ow = OpenWindow(index)
                event_list.append(ow.get_dict())

            elif gt.SCEwords.jitter_sign in line:
                # 判断对话框抖动
                if line.startswith(gt.SCEwords.jitter_sign):
                    if gt.SCEwords.speaker in lis[i+1]:
                        jit = Jitter(index)
                        if gt.SCEwords.time_identifier in line:
                            temp1 = line.find(gt.SCEwords.time_identifier)
                            temp2 = line.find(gt.SCEwords.end_backup, temp1)
                            temp = line[temp1:temp2]
                            time = temp.split('：')[1]
                            if '、' in line:
                                time = time.split('、')[0]
                            jit.time = float(time)
                        event_list.append(jit.get_dict())
                    else:
                        jit = Jitter(index - 1)
                        if gt.SCEwords.time_identifier in line:
                            temp1 = line.find(gt.SCEwords.time_identifier)
                            temp2 = line.find(gt.SCEwords.end_backup, temp1)
                            temp = line[temp1:temp2]
                            time = temp.split('：')[1]
                            if '、' in line:
                                time = time.split('、')[0]
                            jit.time = float(time)
                        event_list.append(jit.get_dict())
                else:
                    jit = Jitter(index - 1)
                    if gt.SCEwords.time_identifier in line:
                        temp1 = line.find(gt.SCEwords.time_identifier)
                        temp2 = line.find(gt.SCEwords.end_backup, temp1)
                        temp = line[temp1:temp2]
                        time = temp.split('：')[1]
                        if '、' in line:
                            time = time.split('、')[0]
                        jit.time = float(time)
                    event_list.append(jit.get_dict())

            elif line.startswith(gt.SCEwords.speaker):
                # 判断对话（有明显说话人提示）
                temp = line.replace(gt.SCEwords.speaker, '')
                talker = temp.replace(gt.SCEwords.end, '')
                body = []
                for j in range(1, search):
                    if i+j >= len(lis) - 1:
                        break
                    lin = lis[i+j]
                    lin = lin.replace('\n', '')
                    lin = lin.replace('\u3000', '')
                    if lin.startswith(gt.SCEwords.chara_voice) and lin == lis[i+1]:
                        temp = line.replace(gt.SCEwords.chara_voice, '')
                        tker = temp.replace(gt.SCEwords.end, '')
                        if tker == talker:
                            talker = tker
                    elif lin.startswith(gt.SCEwords.live2d_appear):
                        continue
                    elif not lin.startswith(gt.SCEwords.start):
                        if '＠' in lin:
                            temp = DialogueSections.__clean_text(lin)
                            body.append(temp)
                        elif lin.startswith('\t'):
                            continue
                        else:
                            temp = lin
                            body.append(temp)
                            continue
                    elif lin.startswith(gt.SCEwords.speaker):
                        break
                    elif lin.startswith(gt.SCEwords.chara_voice) and body != []:
                        break
                    else:
                        continue
                if body == []:
                    continue
                dialogue = Dialogue(index, talker, body)
                dialogue.body = dialogue.build_body()
                event_list.append(dialogue.get_dict())
                index += 1
                
            elif line.startswith(gt.SCEwords.chara_voice) and not gt.SCEwords.speaker in lis[i-1]:
                # 判断对话（仅有voice提示）
                temp = line.replace(gt.SCEwords.chara_voice, '')
                tker = temp.replace(gt.SCEwords.end, '')
                body = []
                if tker == talker:
                    talker = tker
                else:
                    pass
                for j in range(1,search):
                    if i+j >= len(lis) - 1:
                        break
                    lin = lis[i+j]
                    lin = lin.replace('\n', '')
                    lin = lin.replace('\u3000', '')
                    if not lin.startswith(gt.SCEwords.start):
                        if '＠' in lin:
                            temp = DialogueSections.__clean_text(lin)
                            body.append(temp)
                        elif lin.startswith('\t'):
                            continue
                        else:
                            temp = lin
                            body.append(temp)
                            continue
                    elif lin.startswith(gt.SCEwords.live2d_appear):
                        continue
                    elif lin.startswith(gt.SCEwords.speaker):
                        break
                    elif lin.startswith(gt.SCEwords.chara_voice) and body != []:
                        break
                    else:
                        continue
                if body == []:
                    continue
                dialogue = Dialogue(index, talker, body)
                dialogue.body = dialogue.build_body()
                event_list.append(dialogue.get_dict())
                index += 1
            
            else:
                continue
        
        return event_list

    def tl_substitude(template, ev_list):
        '''
        输入翻译模板路径和event list，返回替换翻译后的event list
        '''
        with open(template, 'r', encoding='utf-8') as f:
            tem = f.readlines()

        tmp_li = []
        for tm in tem:
            tm = tm.replace('\n', '')
            tm = tm.split(':')
            tmp_li.append(tm)

        ori_li = []
        for e in ev_list:
            if e['EventType'] == 'Title':
                ori_li.append(e)
            if e['EventType'] == 'Subtitle':
                ori_li.append(e)
            if e['EventType'] == 'Dialogue':
                ori_li.append(e)

        for tmp, ori in zip(tmp_li, ori_li):
            ori['Body'] = tmp[1]

        return ev_list

if __name__ == '__main__':
    pass