import os

'''
这个部分负责文本提取和模板生成
'''

class SCEwords:
    title = '［タイトル：'
    sub_title = '［サブタイトル：'
    speaker = '［話：'
    chara_voice = '［Live2Dキャラボイス：'

    fade_in = '［フェードイン：'
    fade_time = 'フェード：'
    close_window = '［ウインドウ非表示：'
    open_window = '［表示：'
    font_size = '［ウインドウフォントサイズ：'
    jitter_sign = '［ゆれ：ウインドウ1'
    time_identifier = '時間：'
    live2d_appear = '［Live2Dキャラ表示：'
    
    background_name = '［背景DJK：'
    live2d_disappear = '［Live2Dキャラ非表示：'
    live2d_film = '［Live2Dキャラフィルム：'

    event_list = [title, sub_title, speaker]

    start = '［'
    end = '］\n'
    end_backup = '］' # 涉及索引切片操作的时候用这个

class TemplateUtils:
    def __clean_text(text) -> str:
        li = text.split('＠')
        res = li[0] + '\n'
        return res

    def txt_to_template(route):
        '''
        输入文本路径（来自文本清理）
        基于提取的文本生成模板
        '''

        with open(route, 'r+', encoding='utf-8') as original:
            li = original.readlines()

        with open(route, 'w+', encoding='utf-8') as f:
            for i in range(len(li)):
                line = li[i]
                if line.startswith(SCEwords.title):
                    f.write('Title:')
                elif line.startswith(SCEwords.sub_title):
                    f.write('\nSubtitle:')
                elif line.startswith(SCEwords.speaker):
                    line = line.replace(SCEwords.speaker, '\n')
                    line = line.replace(SCEwords.end, ':')
                    f.write(line)
                elif line == '\n':
                    continue
                elif i == len(li) - 1:
                    continue
                else:
                    if li[i+1] != '\n' and SCEwords.start not in li[i]:
                        f.write('\\N')
                    else:
                        continue
                    
    def clean_sce(pth) -> str:
        '''
        输入sce路径，提取文本生成txt
        输出的str是文本路径，给模板生成用的
        '''
        temp_filepath, filename = os.path.split(pth)
        file_sole_name = os.path.splitext(filename)[0]
        txt_name = file_sole_name + '.txt'
        new_filepath = os.path.join(temp_filepath, txt_name)

        if os.path.exists(new_filepath):
            txt_name = file_sole_name + ' - copy' + '.txt'
            new_filepath = os.path.join(temp_filepath, txt_name)
        else:
            pass

        with open(pth, 'r', encoding='utf-8') as sce:
            origin = []
            ori = sce.readlines()
            for o in ori:
                if '＠' in o:
                    s = TemplateUtils.__clean_text(o)
                    origin.append(s)
                elif '{' in o or '}' in o:
                    continue
                elif not o == '\n':
                    origin.append(o)

        def talker_devider(talker):
            tmp = talker.replace(SCEwords.speaker, '')
            talk_person = tmp.replace(SCEwords.end, '')
            return talk_person

        def voice_devider(voicer):
            tmp = voicer.replace(SCEwords.chara_voice, '')
            talk_person = tmp.replace(SCEwords.end, '')
            return talk_person

        def talker_builder(talk_person):
            talker = SCEwords.speaker + talk_person + SCEwords.end
            return talker

        search = 10
        with open(new_filepath, 'w+', encoding='utf-8') as f:
            talker = ''
            talk_person = ''
            for i in range(len(origin)):
                line = origin[i]
                if SCEwords.title in line:
                    line = line[:-1]
                    f.write(line)
                elif SCEwords.sub_title in line:
                    line = '\n' + line
                    f.write(line)
                elif line.startswith('\t'):
                    continue
                elif SCEwords.speaker in line:
                    body = []
                    for j in range(1, search):
                        if i+j >= len(origin):
                            break
                        lin = origin[i+j]
                        if lin.startswith(SCEwords.live2d_appear):
                            continue
                        elif not lin.startswith(SCEwords.start):
                            if '＠' in lin:
                                temp = TemplateUtils.__clean_text(lin)
                                body.append(temp)
                            elif lin.startswith('\t'):
                                continue
                            else:
                                body.append(lin)
                        elif lin.startswith(SCEwords.speaker):
                            break
                        elif lin.startswith(SCEwords.chara_voice) and body != []:
                            break
                        else:
                            continue
                    if body == []:
                        continue
                    else:
                        talker = line
                        talk_person = talker_devider(talker)
                        line = '\n' + line
                        f.write(line)
                elif SCEwords.chara_voice in line and not SCEwords.speaker in origin[i-1]:
                    tker = voice_devider(line)
                    body = []
                    if tker == talk_person:
                        talker = talker_builder(tker)
                    else:
                        pass
                    for j in range(1,search):
                        if i+j >= len(origin):
                            break
                        lin = origin[i+j]
                        if not lin.startswith(SCEwords.start):
                            if '＠' in lin:
                                temp = TemplateUtils.__clean_text(lin)
                                body.append(temp)
                            elif lin.startswith('\t'):
                                continue
                            else:
                                body.append(lin)
                        elif lin.startswith(SCEwords.live2d_appear):
                            continue
                        elif lin.startswith(SCEwords.speaker):
                            break
                        elif lin.startswith(SCEwords.chara_voice) and body != []:
                            break
                        else:
                            continue
                    if body == []:
                        continue
                    else:
                        talk = '\n' + talker
                        f.write(talk)
                elif not SCEwords.start in line:
                    f.write(line)
                else:
                    continue

        return new_filepath
    
    def sce_to_template(pth):
        '''
        输入sce路径，直接生成模板
        '''
        filepath = TemplateUtils.clean_sce(pth)
        TemplateUtils.txt_to_template(filepath)

if __name__ == '__main__':
    pass