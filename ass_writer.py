from dialogue_sections import sce_handler, tl_substitude
from image_sections import image_section_generator, get_tstamp, jitter_cleaner
import ass_utils as au
import settings_handler as sh
import os
import shutil

def ass_writer(sce, video, template=None):
    im_sections, alert_li = jitter_cleaner(image_section_generator(video))
    ev_sections = sce_handler(sce)
    if template != None:
        ev_sections = tl_substitude(template, sce_handler(sce))

    dialogue_list = []
    title_list = []
    change_windows = []
    colorfade_li = []

    ass_dialogue = []
    ass_shader = []
    ass_alert = []

    for d in ev_sections:
        if d['EventType'] == 'Dialogue':
            dialogue_list.append(d)
        if d['EventType'] == 'Title' or d['EventType'] == 'Subtitle':
            title_list.append(d)
        if d['EventType'] == 'CloseWindow':
            change_windows.append(d)

    for ch in change_windows:
        if 'Color' in ch:
            colorfade_li.append(ch['Index'])

    for di, im in zip(dialogue_list, im_sections):
        if 'CloseWindow' in im:
            if 'Color' in ch and im['Index'] in colorfade_li:
                naming = 'BlackFade'
                extra_fad = '{\\fad(0,600)}'
                text_fad = '{\\fad(0,500)}'
            else:
                naming = 'NormalClose'
                extra_fad = '{\\fad(0,50)}'
                text_fad = '{\\fad(0,50)}'
            line = au.Dialogue(get_tstamp(im['Start']), get_tstamp(im['End']), di['Talker'], text = di['Body'] + text_fad)
            shader = au.Shader(get_tstamp(im['Start']), get_tstamp(im['End']), name=naming, text=au.shader_builder(len(di['Talker'])) + extra_fad)
        else:
            line = au.Dialogue(get_tstamp(im['Start']), get_tstamp(im['End']), di['Talker'], di['Body'])
            shader = au.Shader(get_tstamp(im['Start']), get_tstamp(im['End']), text=au.shader_builder(len(di['Talker'])))
        shader = shader.build_comment()
        ass_shader.append(shader)
        line = line.build_dialogue()
        ass_dialogue.append(line)

    for ti in title_list:
        tit_count = int(0)
        title = au.Title(get_tstamp(0), get_tstamp(750), name = 'Title' , text = '{\\fad(100,100)}' + ti['Body'])
        title = title.build_dialogue()
        modify_index = int(tit_count) - 1
        ind = int(ti['Index']) + modify_index
        ass_dialogue.insert(int(ind), title)
        tit_count += int(1)

    for a in alert_li:
        alert = au.Caution(get_tstamp(a['Start']), get_tstamp(a['End']), 'ALERT', 'PLEASE TAKE NOTICE\\NIT MAY BE A JITTER')
        alert = alert.build_comment()
        ass_alert.append(alert)

    src = sh.Settings.settings_reader(sh.Settings.SAMPLE_ASS_PATH)
    route, name = os.path.split(video)
    shutil.copy(src, route)
    old_name = os.path.join(route, src)
    new_name = video.replace('.mp4', '.ass')
    os.rename(old_name, new_name)

    with open(new_name, 'a+', encoding='utf-8') as a:
        for s in ass_shader:
            a.write(s + '\n')
        for al in ass_alert:
            a.write(al + '\n')
        for dial in ass_dialogue:
            a.write(dial + '\n')

    print('Process Completed!')

if __name__ == '__main__':
    scenario = 'C:\\Users\\roma\\Documents\\D4DJ Unpack\\sce\\2000770001.sce'
    vid = 'C:\\Users\\roma\\Documents\\D4DJ Unpack\\tbk\\iphone10_test.mp4'
    #tmpl = 'C:\\Users\\roma\\Documents\\D4DJ Unpack\\tbk\\6010510002.txt'

    ass_writer(scenario, vid)
    #ass_writer(scenario, vid, template=tmpl)