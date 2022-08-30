import numpy as np
import cv2
import settings_handler as sh

class ImageData(object):
    '''
    对一帧进行对话框和文字判定
    '''
    def __init__(self, image) -> None:
        self.image = image

    def is_dialogue(self,x1,x2,y1,y2) -> bool:
        #判断对话框
        self.dialogue = bool(False)
        lower = np.array([159, 70, 180])
        upper = np.array([168, 245, 245])

        im = self.image
        fhsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(fhsv, lower, upper)
        im = cv2.bitwise_and(im, im, mask=mask)
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        ret, im = cv2.threshold(im, 80, 255, cv2.THRESH_BINARY)
        read_result = ImageSections.read_pixel(im, x1, x2, y1, y2)
        if read_result:
            self.dialogue = bool(True)
        return self.dialogue

    def is_word(self,x1,x2,y1,y2) -> bool:
        #判断文字
        self.word = bool(False)
        img = self.image[y1:y2, x1:x2]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, img = cv2.threshold(img, 75, 255, cv2.THRESH_BINARY_INV)
        self.word_nz = np.count_nonzero(img)
        if self.word_nz >= 50:
            self.word = bool(True)
        return self.word

class ImageSections:
    def get_tstamp(milliseconds) -> str:
        '''
        将视频进行时的毫秒数转化为aegisub中的时间戳
        '''
        seconds = milliseconds//1000
        milliseconds = milliseconds%1000

        minutes = 0
        hours = 0
        if seconds >= 60:
            minutes = seconds//60
            seconds = seconds % 60

        if minutes >= 60:
            hours = minutes//60
            minutes = minutes % 60

        hr = str(hours)
        m = str(int(minutes)).zfill(2)
        s = str(int(seconds)).zfill(2)
        ms = str(int(milliseconds))[:-1].zfill(2)

        tstamp = '{}:{}:{}.{}'.format(hr, m, s, ms)
        return tstamp

    def read_pixel(frame, x1, x2, y1, y2):
        '''
        判断四个点是否为白色，如果四个都是，返回true，否则返回false
        '''
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

    def Merge(dict1, dict2): 
        res = {**dict1, **dict2} 
        return res 

    def image_section_generator(vid, width, height):
        '''
        输入视频路径，返回一个包含各节点的列表
        '''
        cap = cv2.VideoCapture(vid)
        image_sections = []
        word_count = 1

        #border
        x1,y1,x2,y2 = sh.Reference.box_splitter(sh.Reference.reference_reader(sh.Reference.TEXT_BORDER_MX, width, height))

        #dialogue
        x_1,y_1,x_2,y_2 = sh.Reference.box_splitter(sh.Reference.reference_reader(sh.Reference.TEXT_WORD_MX, width, height))
        
        cap = cv2.VideoCapture(vid)
        success, p_frame = cap.read()
        prev_frame = ImageData(p_frame)
        prev_frame.dialogue = prev_frame.is_dialogue(x1, x2, y1, y2)
        prev_frame.word = prev_frame.is_word(x_1, x_2, y_1, y_2)

        start = ''
        end = ''
        process_count = 0
        spec = {}

        while success:
            try:
                success, c_frame = cap.read()
                ms = cap.get(cv2.CAP_PROP_POS_MSEC)
                stamp = ImageSections.get_tstamp(ms)
                curr_frame = ImageData(c_frame)
                curr_frame.dialogue = curr_frame.is_dialogue(x1, x2, y1, y2)
                curr_frame.word = curr_frame.is_word(x_1, x_2, y_1, y_2)
                
                if curr_frame.dialogue == prev_frame.dialogue:
                    if curr_frame.dialogue:
                        if curr_frame.word == False and prev_frame.word != curr_frame.word:
                            end = ms
                            process_count += 1
                            if process_count % 8 == 0:    
                                print('Process at: ' + stamp)
                            image_sections.append(ImageSections.Merge({'Index':word_count,'Start':start, 'End':end}, spec))
                            start = ms
                            spec = {}
                            word_count += 1
                else:
                    if curr_frame.dialogue:
                        start = ms
                        spec = {'OpenWindow':True}
                        process_count += 1
                        if process_count % 8 == 0:    
                            print('Process at: ' + stamp)
                    else:
                        end = ms
                        spec = ImageSections.Merge(spec, {'CloseWindow':True})
                        process_count += 1
                        if process_count % 8 == 0:    
                            print('Process at: ' + stamp)
                        image_sections.append(ImageSections.Merge({'Index':word_count,'Start':start, 'End':end}, spec))
                        word_count += 1
                prev_frame = curr_frame
            except cv2.error as e:
                break
        cap.release()

        return image_sections

    def jitter_cleaner(img_sections:list):
        '''
        输入image sections，返回清理后的image sections和警告列表

        清除时间过短的视频分段，合并连续的过段分段并从主列表清除，另添加至警告列表
        '''
        remove_li = []
        for im in img_sections:
            if im['End'] - im['Start'] < 1000.0:
                remove_li.append(im)

        tmp = []
        remove_subli = []
        for r in remove_li:
            img_sections.remove(r)
            if len(remove_subli) == 0 or remove_subli[-1]['Index'] + 1 == r['Index']:
                remove_subli.append(r)
            else:
                if len(remove_subli) >= 2:
                    tmp.append(remove_subli)
                remove_subli = [r]
        if len(remove_subli) >= 2:
            tmp.append(remove_subli)
            remove_subli = []

        alert = []
        count = 0
        for t in tmp:
            start = t[0]['Start']
            end = t[-1]['End']
            alert.append({'Index':count, 'Start':start, 'End':end, 'Jitter':True})

        for i in range(len(img_sections)):
            img = img_sections[i]
            img['Index'] = i+1

        return img_sections, alert

if __name__ == '__main__':
    pass