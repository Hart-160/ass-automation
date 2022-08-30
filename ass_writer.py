from dialogue_sections import DialogueSections
from image_sections import ImageSections
import ass_utils as au
import settings_handler as sh
import os
import cv2
import shutil

def shader_builder(length:int, width, height):
    x1b, x2b = sh.Reference.shader_splitter(sh.Reference.reference_reader(sh.Reference.SCREEN_INITIAL, width, height))
    x3b = x2b
    var = int(sh.Reference.reference_reader(sh.Reference.SCREEN_VARIABLE, width, height))

    x1 = x1b + int(var) * length
    x2 = x2b + int(var) * length
    x3 = x3b + int(var) * length

    effect = '{\\p1}'
    shelter_template = sh.Reference.reference_reader(sh.Reference.SCREEN_TEXT, width, height).format(x1, x2, x3)

    return effect + shelter_template

def write_ass(sce, video, template=None) -> bool:
    cap = cv2.VideoCapture(video)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    cap.release()

    print('Frame Width: {}'.format(width))
    print('Frame Height: {}'.format(height))
    print('FPS: {}'.format(fps))

    ref = sh.AutoRead.get_preferred_ref(width, height)
    if ref == None:
        print('No Reference Found! Please check your source or make presets for your resolution')
        if sh.AutoRead.get_preferred_ref(height, width) != None:
            print('Please check if your source was rotated! Try to make it into the right position!')
        return False
    elif fps < 60:
        print('The program only supports 60hz sources. Please be sure your source supports that!')
        return False
    else:
        print('SampleASS: ' + sh.AutoRead.get_preferred_ass(width, height))
        print('Reference: ' + sh.AutoRead.get_preferred_ref(width, height))
        print('Started...')
        im_sections, alert_li = ImageSections.jitter_cleaner(ImageSections.image_section_generator(video, width, height))
        ev_sections = DialogueSections.sce_handler(sce)
        if template != None:
            ev_sections = DialogueSections.tl_substitude(template, DialogueSections.sce_handler(sce))

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
                open_offset = 0
                if 'OpenWindow' in im:
                    naming = 'OpenClose'
                    open_offset = int(sh.Settings.settings_reader(sh.Settings.OPEN_BOX_OFFSET))

                if 'Color' in ch and im['Index'] in colorfade_li:
                    naming = 'BlackFade'
                    extra_fad = '{\\fad(0,600)}'
                    text_fad = '{\\fad(0,500)}'
                    fade_offset = int(sh.Settings.settings_reader(sh.Settings.BLACK_FADEIN_OFFSET))
                else:
                    naming = 'NormalClose'
                    extra_fad = '{\\fad(0,100)}'
                    text_fad = '{\\fad(0,100)}'
                    fade_offset = int(sh.Settings.settings_reader(sh.Settings.NORMAL_CLOSE_OFFSET))
                line = au.Dialogue(ImageSections.get_tstamp(im['Start'] + open_offset), ImageSections.get_tstamp(im['End'] + fade_offset), di['Talker'], text = text_fad + di['Body'])
                shader = au.Shader(ImageSections.get_tstamp(im['Start'] + open_offset), ImageSections.get_tstamp(im['End'] + fade_offset), name=naming, text=shader_builder(len(di['Talker']), width, height) + extra_fad)
            else:
                open_offset = 0
                naming = None
                if 'OpenWindow' in im:
                    open_offset = int(sh.Settings.settings_reader(sh.Settings.OPEN_BOX_OFFSET))
                    naming = 'OpenWindow'
                    
                line = au.Dialogue(ImageSections.get_tstamp(im['Start'] + open_offset), ImageSections.get_tstamp(im['End']), di['Talker'], di['Body'])
                shader = au.Shader(ImageSections.get_tstamp(im['Start'] + open_offset), ImageSections.get_tstamp(im['End']), name=naming, text=shader_builder(len(di['Talker']), width, height))
            shader = shader.build_comment()
            ass_shader.append(shader)
            line = line.build_dialogue()
            ass_dialogue.append(line)

        for ti in title_list:
            tit_count = int(0)
            title = au.Title(ImageSections.get_tstamp(0), ImageSections.get_tstamp(750), name = 'Title' , text = '{\\fad(100,100)}' + ti['Body'])
            title = title.build_dialogue()
            modify_index = int(tit_count) - 1
            ind = int(ti['Index']) + modify_index
            ass_dialogue.insert(int(ind), title)
            tit_count += int(1)

        for a in alert_li:
            alert = au.Caution(ImageSections.get_tstamp(a['Start']), ImageSections.get_tstamp(a['End']), 'ALERT', 'PLEASE TAKE NOTICE\\NIT MAY BE A JITTER')
            alert = alert.build_comment()
            ass_alert.append(alert)
        
        src = sh.Settings.settings_reader(sh.Settings.SAMPLE_ASS_PATH, width, height)
        route, name = os.path.split(video)
        shutil.copy(src, route)
        old_name = os.path.join(route, src)
        try:
            new_name = video + '.ass'
            os.rename(old_name, new_name)
        except FileExistsError:
            new_name = video + ' - copy' + '.ass'
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
            print('There are {} line(s) shifted. Please take a notice!'.format(abs(len(dialogue_list) - len(im_sections))))
        return True

if __name__ == '__main__':
    pass