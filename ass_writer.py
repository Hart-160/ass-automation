from classifytest import sce_handler
from videotest import image_section_generator, get_tstamp
import utils.ass_param as ap
import os
import shutil

def ass_writer(sce, video):
    ev_sections = sce_handler(sce)
    im_sections = image_section_generator(video)

    dialogue_list = []
    title_list = []
    change_windows = []

    ass_dialogue = []
    ass_shader = []

    '''
    WIP 增加GUI界面，file chooser

    WIP 不同分辨率适配

    WIP 抖动支持
    '''

    for d in ev_sections:
        if d['EventType'] == 'Dialogue':
            dialogue_list.append(d)
        if d['EventType'] == 'Title' or d['EventType'] == 'Subtitle':
            title_list.append(d)
        if d['EventType'] == 'OpenWindow' or d['EventType'] == 'CloseWindow':
            change_windows.append(d)

    for di, im in zip(dialogue_list, im_sections):
        if 'CloseWindow' in im:
            for ch in change_windows:
                if 'Color' in ch and ch['Index'] == im['Index']:
                    end = im['End'] - 100
                    naming = 'BlackFade'
                    extra_fad = '{\\fad(0,600)}'
                    text_fad = '{\\fad(0,500)}'
                    break
                else:
                    end = im['End'] + 50
                    naming = 'NormalClose'
                    extra_fad = '{\\fad(0,50)}'
                    text_fad = '{\\fad(0,50)}'
                    break
            line = ap.Dialogue(get_tstamp(im['Start']), get_tstamp(end), di['Talker'], text = text_fad + di['Body'])
            shader = ap.Shader(get_tstamp(im['Start']), get_tstamp(end), name=naming, text=extra_fad + ap.shader_builder(len(di['Talker'])))
        else:
            line = ap.Dialogue(get_tstamp(im['Start']), get_tstamp(im['End']), di['Talker'], di['Body'])
            shader = ap.Shader(get_tstamp(im['Start']), get_tstamp(im['End']), text=ap.shader_builder(len(di['Talker'])))
        shader = shader.build_comment()
        ass_shader.append(shader)
        line = line.build_dialogue()
        ass_dialogue.append(line)

    for ti in title_list:
        tit_count = 0
        title = ap.Title(get_tstamp(0), get_tstamp(750), name = 'Title' , text = '{\\fad(100,100)}' + ti['Body'])
        title = title.build_dialogue()
        modify_index = int(tit_count) - 1
        ind = ti['Index'] + modify_index
        ass_dialogue.insert(int(ind), title)
        tit_count += 1

    src = '[1920x1440]untitled.ass'
    route, name = os.path.split(video)
    shutil.copy(src, route)
    old_name = os.path.join(route, src)
    new_name = video + '.ass'
    os.rename(old_name, new_name)

    with open(new_name, 'a+', encoding='utf-8') as a:
        for s in ass_shader:
            a.write(s + '\n')
        for dial in ass_dialogue:
            a.write(dial + '\n')

    print('Process Completed!')

if __name__ == '__main__':
    sce_id = 6010510001
    sce = 'C:\\Users\\roma\\Documents\\D4DJ Unpack\\sce\\{}.sce'.format(str(sce_id))
    video = 'C:\\Users\\roma\\Documents\\D4DJ Unpack\\tbk\\tbk_personal1.mp4'

    ass_writer(sce, video)