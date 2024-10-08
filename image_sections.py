import cv2
import os
import shutil
from numpy import array, count_nonzero, argmax, fromstring, uint8, empty
from PySide2.QtCore import QObject, Signal
from PIL import Image, ImageFont, ImageDraw

import settings_handler as sh
from asset_data import B64_Images

'''
这个部分负责分析视频
'''

class TextTemplate(object):

    def generate_text_image(text:str, var:int, suffix=0) -> str:
        if len(text) == 0:
            return
        
        image = Image.new('RGB', (var*len(text)+1, var+1), (0,0,0))
        font = ImageFont.truetype("Aegisub stuffs/FOT-RodinNTLG Pro B.otf", var)
        draw = ImageDraw.Draw(image)

        if not os.path.exists('cache'):
            os.mkdir('cache')
        
        draw.text((0,0), text, 'white', font)
        template_route = f'cache/temp_{suffix}.png'
        
        image.save(template_route)
        
    def generate_text_image_batch(ev_sections, width, height):
        #只适用于カードイラスト表示
        
        dialogue_list = []
        font_size_change_list = []
        for d in ev_sections:
            if d['EventType'] == 'Dialogue':
                dialogue_list.append(d)
            if d['EventType'] == 'FontSizeChange':
                font_size_change_list.append(d)

        talker_list = []
        talker_dict = {}
        text_list = []
        for d in dialogue_list:
            if not d['Talker'] in talker_list:
                talker_list.append(d['Talker'])
            text_list.append({'Index':d['Index'], 'Text':d['Body'][:2]})
        for i in range(len(talker_list)):
            talker_dict[talker_list[i]] = i+1

        var = int(sh.Reference.reference_reader(sh.Reference.SCREEN_VARIABLE, width, height))

        for i in range(len(talker_list)):
            TextTemplate.generate_text_image(talker_list[i], var, f"0{talker_dict[talker_list[i]]}")
        for t in text_list:
            change_index = 1
            for f in font_size_change_list:
                if f['Index'] == t['Index'] and f['FontSize'] != 'Default':
                    change_index = f['FontSize']/48
                    break
            TextTemplate.generate_text_image(t['Text'], int(var*change_index), t['Index'])

        return talker_dict

class ImageData(object):
    '''
    对一帧进行对话框和文字判定
    '''
    def __init__(self, image, lower_range, upper_range, white_threshold, 
                 width, height,
                 word_points:tuple, border_points:tuple, window_type, read_method) -> None:
        self.x1b, self.y1b, self.x2b, self.y2b = border_points
        self.x1w, self.y1w, self.x2w, self.y2w = word_points
        self.method = read_method
        self.window_type = window_type

        self.width = width
        self.height = height

        self.image = image
        if self.method == 'ColorDetect':
            self.gray = self.image[self.y1w:self.y2w, self.x1b-4:self.x2b+4] #定位法
        if self.method == 'TemplateMatch':
            self.gray = self.image[int(height*float(sh.Reference.reference_reader(sh.Reference.TEMPLATE_DETECT_CUT_FACTOR, width, height))):height, 0:width] #模板匹配法
        self.gray = cv2.cvtColor(self.gray, cv2.COLOR_BGR2GRAY)
        self.lower = lower_range
        self.upper = upper_range
        self.white_threshold = white_threshold
        self.word = bool(False)
        self.dialogue = bool(False)
        self.first_letter_mat = empty([0,0])
        self.abs_first_letter_mat = 0

    def __read_pixel(frame, x1, x2, y1, y2):
        #判断四个点是否为白色，如果四个都是，返回true，否则返回false
        yes = 0
        is_dialogue = False
        if frame[y1, x1] == 255:
            yes += 1
        if frame[y2, x1] == 255:
            yes += 1
        if frame[y1, x2] == 255:
            yes += 1
        if frame[y2, x2] == 255:
            yes += 1
        if yes == 4:
            is_dialogue = True
        return is_dialogue
    
    def __is_valid_color(self) -> bool:
        #判断对话框的颜色部分（常规状况下为紫色）
        dialogue = bool(False)

        im = self.image
        im = im[self.y1b:self.y2b, self.x1b:self.x2b]
        fhsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        self.border_color = {'x1':str(fhsv[0, 0]), 'x2':str(fhsv[self.y2b-self.y1b-1, 0]), 'x3':str(fhsv[0, self.x2b-self.x1b-1]), 'x4':str(fhsv[self.y2b-self.y1b-1, self.x2b-self.x1b-1])}
        mask = cv2.inRange(fhsv, array(self.lower), array(self.upper))
        im = cv2.bitwise_and(im, im, mask=mask)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, im = cv2.threshold(im, 80, 255, cv2.THRESH_BINARY)
        read_result = ImageData.__read_pixel(im, 0, self.x2b-self.x1b-1, 0, self.y2b-self.y1b-1)
        if read_result:
            dialogue = bool(True)
        return dialogue

    def __is_valid_white(self):
        #判断对话框外圈的白色部分
        white = bool(False)
        self.border_white = {'x1':str(self.gray[self.y1b-self.y1w-1, 0]), 'x2':str(self.gray[self.y2b-self.y1w-1, 0]), 'x3':str(self.gray[self.y1b-self.y1w-1, self.x2b-self.x1b+7]), 'x4':str(self.gray[self.y2b-self.y1w-1, self.x2b-self.x1b+7])}
        ret, gray = cv2.threshold(self.gray, int(self.white_threshold), 255, cv2.THRESH_BINARY)
        read_result = ImageData.__read_pixel(gray, 0, self.x2b-self.x1b+7, self.y1b-self.y1w-1, self.y2b-self.y1w-1)
        if read_result:
            white = bool(True)
        return white

    def is_dialogue_color(self):
        #定位点颜色识别法
        #结合颜色判定&白色判定输出对话框判定结果
        
        self.valid_color = ImageData.__is_valid_color(self)
        self.valid_white = ImageData.__is_valid_white(self)
        self.dialogue = self.valid_color and self.valid_white
        return self.dialogue

    def set_canny(self, canny):
        self.tmp_canny = canny
    
    def is_dialogue_template(self):
        #模板匹配法
        self.dialogue = bool(False)
        frame_canny = cv2.Canny(self.gray, 300, 500)
        res = cv2.matchTemplate(frame_canny, self.tmp_canny, 5)
        loc = divmod(argmax(res), res.shape[1])
        
        if not (res[loc[0], loc[1]] < 0.3):
            self.dialogue = bool(True)
        return self.dialogue
    #'''

    def __is_true_card_showcase(self, template_image, parameter=''):
        image = self.image
        if parameter == 'name':
            image = image[int(self.height*float(sh.Reference.reference_reader(sh.Reference.CARD_DISPLAY_CUT_UPPER_FACTOR, self.width, self.height))):int(self.height*float(sh.Reference.reference_reader(sh.Reference.CARD_DISPLAY_CUT_LOWER_FACTOR, self.width, self.height))), 0:self.width]
        elif parameter == 'text':
            image = image[int(self.height*float(sh.Reference.reference_reader(sh.Reference.CARD_DISPLAY_CUT_LOWER_FACTOR, self.width, self.height))):self.height, 0:self.width]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        tmp = cv2.imread(template_image)
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        
        res = cv2.matchTemplate(gray, tmp, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        return max_val > 0.7

    def is_dialogue(self, dialogue_list, index=-1, talker_dict=None):
        if self.window_type == 'ウインドウ1':
            if self.method == 'ColorDetect':
                return self.is_dialogue_color()
            if self.method == 'TemplateMatch':
                return self.is_dialogue_template()
        elif "カード" in self.window_type: #カードイラスト表示
            self.dialogue = self.__is_true_card_showcase(f'cache/temp_0{talker_dict[dialogue_list[index-1]["Talker"]]}.png', 'name')
            if not self.dialogue:
                self.dialogue = self.__is_true_card_showcase(f'cache/temp_0{talker_dict[dialogue_list[index]["Talker"]]}.png', 'name')
            return self.dialogue
        else:
            return self.dialogue #False

    def is_word(self, var, dialogue_list, index=-1):
        #判断文字
        if self.window_type == 'ウインドウ1':
            if not self.dialogue:
                return self.word, self.first_letter_mat, self.abs_first_letter_mat
            if self.method == 'ColorDetect':
                img = self.gray[0:self.y2w-self.y1w-1, self.x1w-self.x1b+3:self.x2w-self.x1b+3] #定位法
            elif self.method == 'TemplateMatch':
                img = self.image[self.y1w:self.y2w, self.x1w:self.x2w] #模板匹配法
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #模板匹配法
            ret, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY_INV)
            self.first_letter_mat = img[0:var,var:var*3]
            self.abs_first_letter_mat = count_nonzero(self.first_letter_mat)
            if count_nonzero(img) >= 50:
                self.word = bool(True)
            return self.word, self.first_letter_mat, self.abs_first_letter_mat
        elif "カード" in self.window_type: #カードイラスト表示
            if not self.dialogue:
                return self.word, self.first_letter_mat, self.abs_first_letter_mat
            self.word = self.__is_true_card_showcase(f'cache/temp_{dialogue_list[index-1]["Index"]}.png', 'text')
            return self.word, self.first_letter_mat, self.abs_first_letter_mat
        else:
            return self.word, self.first_letter_mat, self.abs_first_letter_mat

    def get_detailed_data(self, f, ms, window_type):
        #获得详细数据
        if window_type == 'ウインドウ1':
            if self.method == 'ColorDetect':
                return {'Frame':f, 'MiliSecond':ms, 'WindowType':window_type, 'IsValidColor':self.valid_color, 'IsValidWhite':self.valid_white,'IsWord':self.word, 'NonZeroFirstLetter':self.abs_first_letter_mat, 'BorderColor':self.border_color, 'BorderWhite':self.border_white} #定位法
            if self.method == 'TemplateMatch':
                return {'Frame':f, 'MiliSecond':ms, 'WindowType':window_type, 'IsDialogue':self.dialogue,'IsWord':self.word, 'NonZeroFirstLetter':self.abs_first_letter_mat,} #模板匹配法
        elif "カード" in window_type: #カードイラスト表示
            return {'Frame':f, 'MiliSecond':ms, 'WindowType':window_type, 'IsDialogue':self.dialogue,'IsWord':self.word,}

class ImageSections(QObject):
    update_bar = Signal(int) #向GUI发送进度，更新进度条
    setmax = Signal(int)  #向GUI发送进度条最大值，并设置

    COLOR_DETECT = 'ColorDetect' #定位识别法
    TEMPLATE_MATCH = 'TemplateMatch' #模板匹配法

    main_chara_dict = {'りんく': 11, '真秀': 12, 'むに': 13, '麗': 14, 
                       '響子': 21, 'しのぶ': 22, '由香': 23, '絵空': 24, 
                       '咲姫': 31, '衣舞紀': 32, '乙和': 33, 'ノア': 34, 
                       'リカ': 41, '茉莉花': 42, 'さおり': 43, 'ダリア': 44, 
                       '椿': 51, '渚': 52, '緋彩': 53, '葵依': 54, 
                       '美夢': 61, '春奈': 62, '胡桃': 63, 'みいこ': 64, 
                       '愛莉': 71, '茉奈': 72, '紗乃': 73, '灯佳': 74, 
                       'ミチル': 81, 'ルミナ': 82, '心愛': 83, 'はやて': 84, 
                       'ネオ': 91, 'ソフィア': 92, 'エルシィ': 93, 'ヴェロニカ': 94,
                       '詠実': 101, '美鈴': 102, '詩歌': 103, '伊達ちゃん': 104}

    def __Merge(dict1, dict2): 
        res = {**dict1, **dict2} 
        return res 

    def get_template_canny():
        tmp = cv2.cvtColor(B64_Images.get_b64_images(B64_Images.TEMPLATE_B64), cv2.COLOR_BGR2GRAY)
        tmp_canny = cv2.Canny(tmp, 100, 200)
        return tmp_canny

    def image_section_generator(ev_sections, vid, width, height, generate_detailed_data=False, read_method=None):
        '''
        输入视频路径，返回一个包含各节点的列表
        '''
        dialogue_list = []
        window_type_list = []
        
        for d in ev_sections:
            if d['EventType'] == 'Dialogue':
                dialogue_list.append(d)
        
        for d in dialogue_list:
            if not d['WindowType'] in window_type_list:
                window_type_list.append(d['WindowType'])
        
        cap = cv2.VideoCapture(vid)
        total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        pb.setmax.emit(total_frame)

        image_sections = []
        word_count = 1
        
        talker_dict = {}
        for w in  window_type_list:
            if "カード" in w:
                talker_dict = TextTemplate.generate_text_image_batch(ev_sections, width, height)
                break
        
        valid_section_count = 1 #跳帧时用于计算有效section数量
        key_change_frame = 0
        jumped = False

        # data_li是拿来输出更详细的视频读取数据的
        if generate_detailed_data:
            data_li = []

        #border
        border_points = sh.Reference.box_splitter(sh.Reference.reference_reader(sh.Reference.TEXT_BORDER_MX, width, height))

        #dialogue
        word_points = sh.Reference.box_splitter(sh.Reference.reference_reader(sh.Reference.TEXT_WORD_MX, width, height))
        
        #读取设置传入ImageData构造器
        lower_r = sh.Settings.hsv_range_splitter(sh.Settings.settings_reader(sh.Settings.DEFAULT_LOWER_RANGE))
        upper_r = sh.Settings.hsv_range_splitter(sh.Settings.settings_reader(sh.Settings.DEFAULT_UPPER_RANGE))
        white_gate = sh.Settings.settings_reader(sh.Settings.DEFAULT_WHITE_THRESHOLD)

        #传入is_word，此项为单个字的字号，用于截取第一个字的黑白图以比对
        var = int(sh.Reference.reference_reader(sh.Reference.SCREEN_VARIABLE, width, height))

        if read_method == ImageSections.TEMPLATE_MATCH:
            tmp_canny = ImageSections.get_template_canny() #模板匹配法
            x1b, y1b, x2b, y2b = border_points
            resize_factor = (x2b-x1b) / 1486
            tmp_canny = cv2.resize(tmp_canny, (0,0),fx=resize_factor, fy=resize_factor)

        success, p_frame = cap.read()
        f = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        pb.update_bar.emit(f)
        window_type = dialogue_list[valid_section_count-1]['WindowType']
        prev_frame = ImageData(p_frame, lower_r, upper_r, white_gate, width, height, word_points, border_points, window_type, read_method)
        if read_method == ImageSections.TEMPLATE_MATCH:
            prev_frame.set_canny(tmp_canny) #模板匹配法
        prev_frame.dialogue = prev_frame.is_dialogue(dialogue_list, index=valid_section_count, talker_dict=talker_dict)
        prev_frame.word, prev_frame.first_letter_mat, prev_frame.abs_first_letter_mat = prev_frame.is_word(var, dialogue_list, index=valid_section_count)

        start = ''
        end = ''
        spec = {}

        while success:
            try:
                success, c_frame = cap.read()
                ms = cap.get(cv2.CAP_PROP_POS_MSEC)
                f = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                pb.update_bar.emit(f)
                if valid_section_count <= len(dialogue_list):
                    window_type = dialogue_list[valid_section_count-1]['WindowType']
                curr_frame = ImageData(c_frame, lower_r, upper_r, white_gate, width, height, word_points, border_points, window_type, read_method)
                if read_method == ImageSections.TEMPLATE_MATCH:
                    curr_frame.set_canny(tmp_canny) #模板匹配法
                curr_frame.dialogue = curr_frame.is_dialogue(dialogue_list, index=valid_section_count, talker_dict=talker_dict)
                curr_frame.word, curr_frame.first_letter_mat, curr_frame.abs_first_letter_mat = curr_frame.is_word(var, dialogue_list, index=valid_section_count)
                if generate_detailed_data:
                    data_li.append(curr_frame.get_detailed_data(f, ms))
                if curr_frame.dialogue == prev_frame.dialogue:
                    if curr_frame.dialogue:
                        if curr_frame.word == False and prev_frame.word != curr_frame.word:
                            #判断文本更新
                            end = ms
                            key_change_frame = f
                            jumped = False
                            if float(end) - float(start) >= 200:
                                #过滤掉因为白屏造成的过短section
                                image_sections.append(ImageSections.__Merge({'Index':word_count,'Start':start, 'End':end, 'Length':end-start}, spec))
                                if float(end) - float(start) >= 1000.0:
                                    valid_section_count += 1
                                start = ms
                                spec = {}
                                word_count += 1
                        elif (prev_frame.first_letter_mat.any() or curr_frame.first_letter_mat.any()) and not (prev_frame.first_letter_mat == curr_frame.first_letter_mat).all() and prev_frame.abs_first_letter_mat - curr_frame.abs_first_letter_mat > 50:
                            #针对某些录屏，出现切换句子时第一个字直接显示无空白帧的情况
                            end = ms
                            key_change_frame = f
                            jumped = False
                            if float(end) - float(start) >= 200:
                                #过滤掉因为白屏造成的过短section
                                image_sections.append(ImageSections.__Merge({'Index':word_count,'Start':start, 'End':end, 'Length':end-start}, spec))
                                if float(end) - float(start) >= 1000.0:
                                    valid_section_count += 1
                                start = ms
                                spec = {}
                                word_count += 1
                        elif not jumped and f - key_change_frame >= 45:
                            """
                            跳帧备忘：
                            - 游戏内打字机间隔为80ms，换行符为100ms
                            - 无声时打字机出完后会留1000ms换下一行（有声则是声音播完后的1000ms换行）
                            - 有声时说话平均间隔为150ms
                            """
                            
                            talker = dialogue_list[valid_section_count-1]['Talker']
                            text = dialogue_list[valid_section_count-1]['Body']
                            
                            if talker in ImageSections.main_chara_dict:
                                skip_per_char = 2*int(sh.Settings.settings_reader(sh.Settings.SKIP_FRAME_PER_CHARACTER))
                            else:
                                skip_per_char = int(sh.Settings.settings_reader(sh.Settings.SKIP_FRAME_PER_CHARACTER))
                                
                            enter_count = text.count('\\N')
                            text_length = len(text) - enter_count*3
                            jump_time = float(skip_per_char * text_length + 90 * enter_count)
                            jump_frame = int((jump_time / 1000.0) * 60)
                            for i in range(jump_frame):
                                success = cap.grab()
                                pb.update_bar.emit(f+i)
                            
                            jumped = True
                            continue
                else:
                    if curr_frame.dialogue:
                        #前一帧不是对话框，当前帧是对话框，判断对话框出现
                        start = ms
                        key_change_frame = f
                        jumped = False
                        spec = {'OpenWindow':True}
                    else:
                        #前一帧是对话框，当前帧不是对话框，判断对话框消失
                        end = ms
                        key_change_frame = f
                        jumped = False
                        spec = ImageSections.__Merge(spec, {'CloseWindow':True})
                        image_sections.append(ImageSections.__Merge({'Index':word_count,'Start':start, 'End':end, 'Length':end-start}, spec))
                        word_count += 1
                        if float(end) - float(start) >= 1000.0:
                            valid_section_count += 1
                prev_frame = curr_frame
            except cv2.error:
                pb.update_bar.emit(total_frame)
                break
            except TypeError:
                pb.update_bar.emit(total_frame)
                break
        cap.release()
        if os.path.exists('cache'):
            shutil.rmtree('cache')

        if generate_detailed_data:
            return image_sections, data_li
        else:
            return image_sections

    def jitter_cleaner(img_sections:list):
        '''
        输入image sections，返回清理后的image sections和警告列表

        清除时间过短的视频分段，合并连续的过段分段并从主列表清除，另添加至警告列表
        '''

        #清除时长小于1秒的section
        remove_li = []
        for im in img_sections:
            if im['End'] - im['Start'] < 1000.0:
                remove_li.append(im)

        #合并多个连续的小于一秒的section
        tmp = []
        remove_subli = []
        for r in remove_li:
            img_sections.remove(r)
            if len(remove_subli) == 0 or remove_subli[-1]['Index'] + 1 == r['Index']:
                if len(remove_subli) > 0 and r['Start'] - remove_subli[-1]['End'] >= 600:
                    #过滤掉间隔时间过长的连续短section
                    continue
                else:
                    remove_subli.append(r)
            else:
                if len(remove_subli) >= 2:
                    tmp.append(remove_subli)
                remove_subli = [r]
        if len(remove_subli) >= 2:
            tmp.append(remove_subli)
            remove_subli = []

        #将合并的连续短section整合，另外添加至警告列表内
        alert = []
        count = 0
        for t in tmp:
            start = t[0]['Start']
            end = t[-1]['End']
            if end - start >= 100:
                alert.append({'Index':count, 'Start':start, 'End':end, 'Jitter':True})

        for i in range(len(img_sections)):
            img = img_sections[i]
            img['Index'] = i+1

        return img_sections, alert

pb = ImageSections() #为GUI信号输出创建的实例

if __name__ == '__main__':
    pass