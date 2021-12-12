from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
import time
from io import StringIO
from html.parser import HTMLParser
from selenium.webdriver.common.action_chains import ActionChains
from IPython.core.display import display, HTML
display(HTML("<style>div.output_area pre {white-space: pre;}</style>"))


## need to investigate the meaning of those keys
CHROME_DRIVER_PATH = '/Users/nghinguyen/Desktop/asset/chromedriver'
post_content = 'rq0escxv l9j0dhe7 du4w35lb hybvsw6c io0zqebd m5lcvass fbipl8qg nwvqtn77 k4urcfbm ni8dbmo4 stjgntxs sbcfpzgs'
text_content = 'ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a'
image_content = 'l9j0dhe7'
us = ''
ps = ''

time_content = 'tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41'
quality_content = 'bp9cbjyn m9osqain j83agx80 jq4qci2q bkfpd7mw a3bd9o3v kvgmc6g5 wkznzc2l oygrvhab dhix69tm jktsbyx5 rz4wbd8a osnr6wyh a8nywdso s1tcr66n'

see_more_class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p'

scroll_number = 10
scroll_delay = 3

list_groups = [
'https://www.facebook.com/groups/groupgiaodich/',
'https://www.facebook.com/groups/311314533925413/',
'https://www.facebook.com/groups/125253729673696/',
'https://www.facebook.com/groups/475147223546856/',
'https://www.facebook.com/groups/495266428457496/',
'https://www.facebook.com/groups/880510156139794/',
'https://www.facebook.com/groups/289458249585309/',``
'https://www.facebook.com/groups/vnmkmarket/',
'https://www.facebook.com/groups/congdongbanphimco/',
'https://www.facebook.com/groups/507295559626595/',
'https://www.facebook.com/groups/268725360199392/',
'https://www.facebook.com/groups/chogaminggear/',
'https://www.facebook.com/groups/chogaminggear/',
'https://www.facebook.com/groups/236875106689710/',
'https://www.facebook.com/groups/VietNamMechKey/',
'https://www.facebook.com/groups/VietnamKeyboardGroup/',
'https://www.facebook.com/groups/akkovn/',
'https://www.facebook.com/groups/keychronvn/',
'https://www.facebook.com/groups/gearlogitech/',
'https://www.facebook.com/groups/dongphimco/',
'https://www.facebook.com/groups/380419976208835/',
'https://www.facebook.com/groups/banphimcogiare/',
'https://www.facebook.com/groups/181768129374914/',
'https://www.facebook.com/groups/btbnsmechanicalkeyboard/',
'https://www.facebook.com/groups/banphimmaytinh/']
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_num_cm(value):
    cm = 0
    if value.split(" ")[0].isnumeric():
        cm = int(value.split(" ")[0])
    sh = 0
    if 'share' in value:
        sh = int(value.split(" ")[1][len('comments'):])
    return cm,sh

driver = webdriver.Chrome(CHROME_DRIVER_PATH)


driver.get('https://fb.com')
email_element = driver.find_element(By.XPATH, "//input[@id='email']")
email_element.send_keys(us)

pass_element = driver.find_element(By.XPATH, "//input[@id='pass']")
pass_element.send_keys(ps)

l_button = driver.find_element(By.XPATH, "//button[@name='login']")
l_button.click()

from openpyxl import Workbook
wb = Workbook()

# grab the active worksheet
ws = wb.active



for group in list_groups:
    print('go ' + group)
    group_name = group
    driver.get(group)
    
    ## handle scroll
    for i in range(0, scroll_number):
        print('scroll')
        time.sleep(scroll_delay)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    
    
    ## click all see more
    links = driver.find_elements(By.XPATH, "//div[@class='" + see_more_class + "']")
    for i in range(0, len(links)):
        try:
            driver.execute_script("arguments[0].click();", links[i]);
        except Exception as e:
            print('click next e')
        time.sleep(3)
        
    ## get contents:
    list_posts = driver.find_elements(By.XPATH, "//div[@class='" + post_content + "']")
    
    for i in range(0, len(list_posts)):
        texts = list_posts[i].find_elements(By.XPATH, ".//div[@class='" + text_content + "']")
        if(len(texts) > 0 and strip_tags(texts[0].get_attribute('innerHTML')) != ""):
            text_result = ''
            for text in texts:
                text_result += strip_tags(text.get_attribute('innerHTML'))

            time_element = list_posts[i].find_elements(By.XPATH, ".//span[@class='" + time_content + "']")
            time_result = strip_tags(time_element[0].get_attribute('innerHTML'))

            quality = list_posts[i].find_elements(By.XPATH, ".//div[@class='" + quality_content + "']")
            quality_result = ''
            num = 0
            cm = 0
            if(len(quality) > 0):
                print(strip_tags(quality[0].get_attribute('innerHTML')))
                quality_result = strip_tags(quality[0].get_attribute('innerHTML'))
                num, cm = get_num_cm(quality_result)

            wb_result = [group_name, time_result,text_result, quality_result, num, cm]

            images_box  = list_posts[i].find_elements(By.XPATH, ".//div[@class='" + image_content + "']")
            img_result = []
            for j in range(0, len(images_box)):
                images = images_box[j].find_elements(By.XPATH, ".//img")
                for img in images:
                    url = img.get_attribute('src')
                    if 'https' in url:
                        img_result.append(url)
                        wb_result.append('=IMAGE("'+url+'")')
            ws.append(wb_result)
        