import os
from utils.generate_tmp import SCEwords

def fill_title(text) -> str:
    text = text[:-1]
    title = SCEwords.title + text + SCEwords.end
    return title

def fill_subtitle(text) -> str:
    text = text[:-1]
    subtitle = SCEwords.sub_title + text + SCEwords.end
    return subtitle

def sce_substitude(txt, sce):
    pth, filename = os.path.split(sce)
    new_filename = '[AUTO] ' + filename
    new_sce = os.path.join(pth, new_filename)
    if os.path.exists(new_sce):
        sole, extension = os.path.splitext(filename)
        f_n = sole + ' - copy' + extension
        new_filename = '[AUTO] ' + f_n
        new_sce = os.path.join(pth, new_filename)
    else:
        pass
    
    with open(txt, 'r+', encoding='utf-8') as t:
        t_li = t.readlines()
    with open(sce, 'r+', encoding='utf-8') as s:
        s_li = s.readlines()

    event_index = []

    for i in range(len(s_li)):
        for e in SCEwords.event_list:
            if e in s_li[i]:
                event_index.append(i)
        if SCEwords.chara_voice in s_li[i] and s_li[i-1] == '\n':
            event_index.append(i)

    for j in range(len(t_li)):
        e_i = event_index[j]
        if SCEwords.title in s_li[e_i]:
            body = t_li[j].split(':')[1]
            temp1 = fill_title(body)
            s_li[e_i] = temp1
        elif SCEwords.sub_title in s_li[e_i]:
            body = t_li[j].split(':')[1]
            temp2 = fill_subtitle(body)
            s_li[e_i] = temp2
        elif SCEwords.chara_voice in s_li[e_i] and not SCEwords.speaker in s_li[e_i - 1]:
            temp3 = s_li[e_i + 1]
            temp3 = body
            s_li[e_i + 1] = temp3
        elif SCEwords.speaker in s_li[e_i]:
            if SCEwords.chara_voice in s_li[e_i + 1]:
                body = t_li[j].split(':')[1]
                temp4 = s_li[e_i + 2]
                temp4 = body
                s_li[e_i + 2] = temp4
            else:
                body = t_li[j].split(':')[1]
                temp5 = s_li[e_i + 1]
                temp5 = body
                s_li[e_i + 1] = temp5

    new_li = []
    newline_sign = '\\N'
    newline_count = 0
    tmp1 = ''
    tmp2 = ''

    for k in range(len(s_li)):
        tmp1 = ''
        tmp2 = ''
        tmp3 = ''
        if newline_sign in s_li[k]:
            new_li.append(s_li[k])
            newline_count = 0
            newline_count = s_li[k].count(newline_sign)
            if newline_count != 0 and newline_count == 1:
                tmp1 = s_li[k+1]
            elif newline_count != 0 and newline_count == 2:
                tmp2 = s_li[k+1]
                tmp3 = s_li[k+2]
        elif s_li[k] == tmp1 or s_li[k] == tmp2 or s_li[k] == tmp3:
            continue
        else:
            new_li.append(s_li[k])

    for l in range(len(new_li)):
        if '{' in new_li[l]:
            continue
        elif new_li[l-1] != '\n' and not SCEwords.start in new_li[l-1]:
            temp = new_li[l]
            temp = '\n'
            new_li[l] = temp
        elif SCEwords.start not in new_li[l] and new_li[l-1] == '\n' and new_li[l+1] == '\n':
            tp = new_li[l]
            tp = '\n'
            new_li[l] = tp

    with open(new_sce, 'w+', encoding='utf-8') as fi:
        for n in new_li:
            fi.writelines(n)