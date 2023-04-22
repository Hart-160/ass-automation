import os.path

'''
这个部分负责文本提取和模板生成
'''

class SCEwords:
    #重要的标识符
    title = '［タイトル：'
    sub_title = '［サブタイトル：'
    speaker = '［話：'
    chara_voice = '［Live2Dキャラボイス：'

    fade_in = '［フェードイン：'
    fade_time = 'フェード：'
    close_window = '［ウインドウ非表示：'
    open_window = '［表示：ウインドウ1'
    font_size = '［ウインドウフォントサイズ：'
    jitter_sign = '［ゆれ：ウインドウ1'
    time_identifier = '時間：'
    amplitude_identifier = '幅：'
    live2d_appear = '［Live2Dキャラ表示：'
    
    #需要去除的标识符
    background_name = '［背景DJK：'
    live2d_disappear = '［Live2Dキャラ非表示：'
    live2d_film = '［Live2Dキャラフィルム：'
    bgm_notice = '［音BGM'
    se_notice = '［音SE'
    wait = '［待：'
    sync_start = '［@Parallel：'
    sync_end = '［@End：'
    
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
            write_data = ''
            for i in range(len(li)):
                line = li[i]
                if line.startswith(SCEwords.title):
                    write_data += 'Title:'
                elif line.startswith(SCEwords.sub_title):
                    write_data += '\nSubtitle:'
                elif line.startswith(SCEwords.speaker):
                    line = line.replace(SCEwords.speaker, '\n')
                    line = line.replace(SCEwords.end, ':')
                    write_data += line
                elif line == '\n':
                    continue
                elif i == len(li) - 1:
                    continue
                else:
                    if li[i+1] != '\n' and SCEwords.start not in li[i]:
                        write_data += '\\N'
                    else:
                        continue
            if write_data.startswith('\n'):
                write_data = write_data.replace('\n', '', 1)
            f.write(write_data)
                    
    def clean_sce(pth) -> str:
        '''
        输入sce路径，提取文本生成txt
        输出的str是文本路径，给模板生成用的
        '''
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
        
        temp_filepath, filename = os.path.split(pth)
        file_sole_name = os.path.splitext(filename)[0]
        txt_name = file_sole_name + '.txt'
        new_filepath = os.path.join(temp_filepath, txt_name)

        if os.path.exists(new_filepath):
            txt_name = file_sole_name + ' - copy' + '.txt'
            new_filepath = os.path.join(temp_filepath, txt_name)
        else:
            pass

        lees = []
        with open(pth, 'r+', encoding='utf-8') as s:
            li = s.readlines()
        
        subli = []
        for l in li:
            if l == '\n':
                lees.append(subli)
                subli = []
            else:
                subli.append(l)
        lees.append(subli)
        
        lis = []
        for lee in lees:
            if lee != []:
                lis.append(lee)

        write_data = ''
        talker = ''
        for block in lis:
            write_body = []
            for line in block:
                if SCEwords.title in line:
                    write_body.append(line)
                elif SCEwords.sub_title in line:
                    write_body.append(line)
                elif line.startswith(SCEwords.speaker):
                    write_body.append(line)
                    talker = talker_devider(line)
                elif line.startswith(SCEwords.chara_voice):
                    voicer = voice_devider(line)
                    if voicer == talker:
                        talker = voicer
                elif line.startswith('\t'):
                    continue
                elif line.startswith('\ufeff{ Main'):
                    continue
                elif not line.startswith(SCEwords.start):
                    if '＠' in line:
                        temp = TemplateUtils.__clean_text(line)
                        write_body.append(temp)
                    else:
                        temp = line
                        write_body.append(temp)
                else:
                    continue
            
            if write_body == []:
                continue

            if not write_body[0].startswith(SCEwords.start):
                talk_person = talker_builder(talker)
                write_body.insert(0, talk_person)
            
            write_body[-1] = write_body[-1] + '\n'
            j = ''
            write_str = j.join(write_body)
            write_data += write_str

        with open(new_filepath, 'w+', encoding='utf-8') as f:
            f.write(write_data)

        return new_filepath
    
    def sce_to_template(pth):
        '''
        输入sce路径，直接生成模板
        '''
        filepath = TemplateUtils.clean_sce(pth)
        TemplateUtils.txt_to_template(filepath)

if __name__ == '__main__':
    pass