from dialogue_sections import sce_handler, tl_substitude
from image_sections import image_section_generator, get_tstamp, jitter_cleaner
import ass_utils as au
import settings_handler as sh
import os
import cv2
import shutil

def write_ass(sce, video, template=None) -> bool:
    print('Started...')

    cap = cv2.VideoCapture(video)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    ref = sh.AutoRead.get_preferred_ref(width, height)
    if ref == None:
        print('No Reference Found! Please check your source or make presets for your resolution')
        return False
    else:
        print('SampleASS: ' + sh.AutoRead.get_preferred_ass(width, height))
        print('Reference: ' + sh.AutoRead.get_preferred_ref(width, height))
        im_sections, alert_li = jitter_cleaner(image_section_generator(video, width, height))
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
                    offset = int(sh.Settings.settings_reader(sh.Settings.BLACK_FADEIN_OFFSET))
                else:
                    naming = 'NormalClose'
                    extra_fad = '{\\fad(0,100)}'
                    text_fad = '{\\fad(0,100)}'
                    offset = int(sh.Settings.settings_reader(sh.Settings.NORMAL_CLOSE_OFFSET))
                line = au.Dialogue(get_tstamp(im['Start']), get_tstamp(im['End'] + offset), di['Talker'], text = text_fad + di['Body'])
                shader = au.Shader(get_tstamp(im['Start']), get_tstamp(im['End'] + offset), name=naming, text=au.shader_builder(len(di['Talker']), width, height) + extra_fad)
            else:
                if 'OpenWindow' in im:
                    offset = int(sh.Settings.settings_reader(sh.Settings.OPEN_BOX_OFFSET))
                else:
                    offset = 0
                line = au.Dialogue(get_tstamp(im['Start'] + offset), get_tstamp(im['End']), di['Talker'], di['Body'])
                shader = au.Shader(get_tstamp(im['Start'] + offset), get_tstamp(im['End']), text=au.shader_builder(len(di['Talker']), width, height))
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
        
        src = sh.Settings.settings_reader(sh.Settings.SAMPLE_ASS_PATH, width, height)
        route, name = os.path.split(video)
        shutil.copy(src, route)
        old_name = os.path.join(route, src)
        new_name = video + '.ass'
        os.rename(old_name, new_name)

        with open(new_name, 'a+', encoding='utf-8') as a:
            for s in ass_shader:
                a.write(s + '\n')
            for al in ass_alert:
                a.write(al + '\n')
            for dial in ass_dialogue:
                a.write(dial + '\n')

        print('Completed!')
        if len(im_sections) != len(dialogue_list):
            print('There is {} line shifted. Please take a notice!'.format(abs(len(dialogue_list) - len(im_sections))))
        return True

if __name__ == '__main__':
    pass