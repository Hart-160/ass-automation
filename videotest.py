import numpy as np
import cv2

def get_tstamp(milliseconds) -> str:
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

class ImageData(object):
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
        read_result = read_pixel(im, x1, x2, y1, y2)
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
        if self.word_nz != 0:
            self.word = bool(True)
        return self.word

def image_section_generator(vid):
    '''
    输入视频路径，返回一个包含各节点的列表
    暂不支持包含抖动的视频
    '''
    word_thresh = 250

    image_sections = []
    section_index = 0
    word_count = 1

    #dialogue
    x1 = 217
    y1 = 1210
    x2 = 1702
    y2 = 1324

    #word
    x_1 = 243
    y_1 = 1183
    x_2 = 1652
    y_2 = 1380
    
    cap = cv2.VideoCapture(vid)
    success, p_frame = cap.read()
    prev_frame = ImageData(p_frame)
    prev_frame.dialogue = prev_frame.is_dialogue(x1, x2, y1, y2)
    prev_frame.word = prev_frame.is_word(x_1, x_2, y_1, y_2)

    start = ''
    end = ''

    while success:
        try:
            success, c_frame = cap.read()
            ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            stamp = get_tstamp(ms)
            curr_frame = ImageData(c_frame)
            curr_frame.dialogue = curr_frame.is_dialogue(x1, x2, y1, y2)
            curr_frame.word = curr_frame.is_word(x_1, x_2, y_1, y_2)
            word_nz = prev_frame.word_nz - curr_frame.word_nz
            
            if curr_frame.dialogue == prev_frame.dialogue:
                if curr_frame.dialogue:
                    if prev_frame.word != curr_frame.word and word_nz > word_thresh:
                        end = ms
                        print('Got ' + stamp)
                        image_sections.append({'Index':word_count,'Start':start, 'End':end})
                        start = ms
                        word_count += 1
            else:
                if curr_frame.dialogue:
                    start = ms
                    print('Got ' + stamp)
                else:
                    end = ms
                    print('Got ' + stamp)
                    image_sections.append({'Index':word_count,'Start':start, 'End':end, 'CloseWindow':True})
                    word_count += 1
            prev_frame = curr_frame
        except cv2.error as e:
            break
    cap.release()

    return image_sections

# 243,1183 1652,1380 x1 y1 x2 y2 (ipad air3) 文本框部分
# 217 1210 1702 1324 四个点在文本框上

if __name__ == '__main__':

    video = 'C:\\Users\\roma\\Documents\\D4DJ Unpack\\tbk\\tbk_personal2.mp4'

    image_sec = image_section_generator(video)
    print(image_sec)