import base64
import copy
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC


class request():
    def __init__(self):
        self.user='15982317940'
        self.pwd='LONGHUAN'
        self.browser=webdriver.Firefox()
        self.url='https://passport.bilibili.com/login'
    def get_request(self):
        self.browser.get(self.url)
        inPut_user=wait.WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((
                By.XPATH,'//*[@id="login-username"]'
            ))
        )
        inPut_user.send_keys(self.user)
        inPut_pwd=wait.WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((
                By.XPATH,'//*[@id="login-passwd"]'
            ))
        )
        inPut_pwd.send_keys(self.pwd)
        login_batten=wait.WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((
                By.XPATH,'//a[@class="btn btn-login"]'
            ))
        )
        login_batten.click()
        time.sleep (3)
        login_batten.click()
        time.sleep (3)
        print("输入账号成功")
    def bg_image(self):
        js='return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png");'
        bg_image_base64=self.browser.execute_script(js).split(',')[1]
        bg_image_bytes=base64.b64decode(bg_image_base64)
        bg_image=Image.open(BytesIO(bg_image_bytes))
        return bg_image

    def slider(self,offsetX):
        slider=wait.WebDriverWait(self.browser,5).until(
            EC.presence_of_element_located((
                By.XPATH,'/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]/div[2]'
            ))
        )
        ActionChains (self.browser).click_and_hold (on_element=slider).perform ( )
        ActionChains (self.browser).move_by_offset (xoffset=offsetX / 2, yoffset=0).perform ( )
        time.sleep (0.5)
        ActionChains (self.browser).move_by_offset (xoffset=offsetX / 2, yoffset=0).perform ( )
        time.sleep (1)  # 拟人操作
        ActionChains (self.browser).release ( ).perform ( )









class VeriImageUtil():
    def __init__(self):
        self.defaultConfig={
            'grayOffset':15,
            'opaque':1,
            'minVerticalLineCount':10
        }
        self.config=copy.deepcopy(self.defaultConfig)
    def updateConfig(self,config):
        for k in self.config:
            if k in config.keys():
                self.config[k]=config[k]
    def getMaxOffset(self,*args):
        av=sum(args)/len(args)
        maxOffset=0
        for a in args:
            offset=abs(av-a)
            if offset>maxOffset:
                maxOffset=offset
        return maxOffset
    def isGrayPx(self,r,g,b):
        return self.getMaxOffset(r,g,b)<self.config['grayOffset']
    def isDarkStyle(self,r,g,b):
        return r<128 and g<128 and b<128
    def isOpaque(self,px):
        return px[3]>=255*self.config['opaque']
    def getVerticalLineOffsetX(self,bgImage):
        bgBytes=bgImage.load()
        x=0
        while x<bgImage.size[0]:
            y=0
            verticalLineCount=0
            while y<bgImage.size[1]:
                px=bgBytes[x,y]
                r=px[0]
                g=px[1]
                b=px[2]
                if self.isDarkStyle(r,g,b) and self.isGrayPx(r,g,b) and self.isOpaque(px):
                    verticalLineCount +=1
                else:
                    verticalLineCount=0
                    y+=1
                    continue
                if verticalLineCount>=self.config['minVerticalLineCount']:
                    return x
                y+=1
            x+=1
        #pass
if __name__=='__main__':
    request=request()
    request.get_request()
    bgImage=request.bg_image()
    veriImageUtil=VeriImageUtil()
    bgOffsetX=veriImageUtil.getVerticalLineOffsetX(bgImage)
    print('bgOffsetX:{}'.format(bgOffsetX))
    request.slider(bgOffsetX-8)
    print('ok')

