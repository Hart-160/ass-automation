import utils.classtest as ct
import utils.generate_tmp as gt

def clean_text(text:str) -> str:
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
        if l != '\n':
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
                tit = ct.Title(index, body)
            else:
                tit = ct.Subtitle(index, body)
            event_list.append(tit.get_dict())

        elif gt.SCEwords.close_window in line:
            # 判断对话框消失
            if gt.SCEwords.fade_in in lis[i-1]:
                # 带有颜色变化的对话框消失
                cw = ct.CloseWindow(index - 1, 'CloseWindow')
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
                cw = ct.CloseWindow(index - 1)
            if event_list[-1]['EventType'] == 'CloseWindow':
                continue
            event_list.append(cw.get_dict())

        elif gt.SCEwords.open_window in line:
            # 判断对话框弹出
            ow = ct.OpenWindow(index)
            event_list.append(ow.get_dict())

        elif gt.SCEwords.jitter_sign in line:
            # 判断对话框抖动
            if line.startswith(gt.SCEwords.jitter_sign):
                if gt.SCEwords.speaker in lis[i+1]:
                    jit = ct.Jitter(index)
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
                    jit = ct.Jitter(index - 1)
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
                jit = ct.Jitter(index - 1)
                if gt.SCEwords.time_identifier in line:
                    temp1 = line.find(gt.SCEwords.time_identifier)
                    temp2 = line.find(gt.SCEwords.end_backup, temp1)
                    temp = line[temp1:temp2]
                    time = temp.split('：')[1]
                    if '、' in line:
                        time = time.split('、')[0]
                    jit.time = float(time)
                event_list.append(jit.get_dict())

            '''
            elif gt.SCEwords.font_size in line:
                # 判断字体大小变化
                temp = line.replace(gt.SCEwords.font_size, '')
                fs = temp.replace(gt.SCEwords.end, '')
                font_size = ct.FontSizeChange(index, fs)
                event_list.append(font_size.get_dict())
            '''

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
                        temp = clean_text(lin)
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
            dialogue = ct.Dialogue(index, talker, body)
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
                        temp = clean_text(lin)
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
            dialogue = ct.Dialogue(index, talker, body)
            dialogue.body = dialogue.build_body()
            event_list.append(dialogue.get_dict())
            index += 1
        
        else:
            continue
    
    return event_list

def snippet_sections_builder(event_li):
    '''
    输入event_list，返回snippet sections列表供image sections对比
    '''
    li = []
    res = []
    section_index = 0
    for event in event_li:
        if event['EventType'] == 'OpenWindow' or event['EventType'] == 'CloseWindow' or event['EventType'] == 'Jitter':
            li.append(event)
    for i in range(len(li)):
        line = li[i]
        if line['EventType'] == 'CloseWindow':
            if li[i-1]['EventType'] != 'Jitter':
                word_count = line['Index'] - li[i-1]['Index'] + 1
                if line['Index'] == li[i-1]['Index']:
                    word_count = 1
                elif li[i-1]['EventType'] == 'OpenWindow' and line['Index'] - li[i-1]['Index'] == 1:
                    word_count = 2
                section_index += 1
                section = {'Index':section_index, 'WordCount':word_count}
                res.append(section)
            else:
                if li[i-1]['EventType'] != 'OpenWindow' and line['Index'] == li[i-1]['Index']:
                    continue
                word_count = line['Index'] - li[i-1]['Index']
                if line['Index'] - li[i-1]['Index'] == 1:
                    word_count += 1
                section_index += 1
                section = {'Index':section_index, 'WordCount':word_count}
                res.append(section)
        elif line['EventType'] == 'Jitter':
            word_count = line['Index'] - li[i-1]['Index'] + 1
            if li[i-1]['EventType'] == 'OpenWindow' and line['Index'] == li[i-1]['Index']:
                continue
            if line['Index'] == li[i-1]['Index']:
                word_count = 1
            elif li[i-1]['EventType'] == 'Jitter':
                word_count -= 1
            section_index += 1
            section = {'Index':section_index, 'WordCount':word_count}
            res.append(section)

    return res

if __name__ == '__main__':
    
    sce_id = 6010510001

    sce = 'C:\\Users\\roma\\Documents\\D4DJ Unpack\\sce\\{}.sce'.format(str(sce_id))
    try:
        event_list = sce_handler(sce)
        #print(event_list)
        for e in event_list:
            print(e)

    except FileNotFoundError:
        print('SCE does not exist!')
