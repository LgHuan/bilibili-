import base64
import time
from io import BytesIO
#bytesio 是基于内存的io读写方式
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Bilibili():
    def __init__(self,user,pwd):
        self.user=user
        self.pwd=pwd
        self.browser=webdriver.Firefox()
        self.wait=WebDriverWait(self.browser,50)
        self.url='https://passport.bilibili.com/login'
    def open(self):
        #输入账号和密码
        self.browser.get(self.url)
        input_user=self.wait.until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="login-username"]'))
        )
        input_user.send_keys(self.user)
        input_pwd=self.wait.until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="login-passwd"]'))
        )
        input_pwd.send_keys(self.pwd)
        login_butten=self.wait.until(
            EC.presence_of_element_located((By.XPATH,'//a[@class="btn btn-login"]'))
        )
        login_butten.click()
        time.sleep (3)
        login_butten.click()
        time.sleep (3)#有时第一次betten_click滑动验证码弹不出来，因此第二次点击，增加验证码弹出机率
        #login_butten1 = self.browser.find_element_by_xpath ('//a[@class="btn btn-login"]')
        print('账号密码输入成功')
    def get_geetest_img(self):
        # 无阴影图片数据
        #js=javascript下载数据base64编码方式,再转为二进制数据,最后用打开图片方式打开
        js = 'return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png");'
        complete_img_data=self.browser.execute_script(js)
        complete_img_base64=complete_img_data.split(',')[1]
        complete_img=base64.b64decode(complete_img_base64)
        c_image=Image.open(BytesIO(complete_img))
        c_image.save('c_image.png')
        #有阴影图片数据
        js='return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png");'
        incomplete_img_data=self.browser.execute_script(js)
        incomplete_img_base64=incomplete_img_data.split(',')[1]
        incomplete_img=base64.b64decode(incomplete_img_base64)
        ic_image=Image.open(BytesIO(incomplete_img))
        ic_image.save('ic_image.png')

        return c_image,ic_image

    def is_pixel_similar(self,c_image,ic_image,x,y):
        #【x,y】返回图片的像素信息
        c_pixel=c_image.load()[x,y]
        ic_pixel=ic_image.load()[x,y]
        threshold=10
        #原图的像素信息和有阴影图相比较，允许误差threshold
        if abs(c_pixel[0]-ic_pixel[0])<threshold and \
            abs(c_pixel[1]-ic_pixel[1])<threshold and \
            abs(c_pixel[2]-ic_pixel[2])<threshold:
            return True
        return False
    def get_slice_gap(self,c_image,ic_image):
        for x in range(c_image.size[0]):
            for y in range(ic_image.size[1]):
                if not self.is_pixel_similar(c_image,ic_image,x,y):
                    return x
    def drag_slider(self,gap):
        slider=self.wait.until(
            EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]/div[2]'))
        )
        #actionchains 鼠标操作
        ActionChains(self.browser).click_and_hold(on_element=slider).perform()
        ActionChains(self.browser).move_by_offset(xoffset=gap/2,yoffset=0).perform()
        time.sleep(0.5)
        ActionChains (self.browser).move_by_offset (xoffset=gap/2, yoffset=0).perform ( )
        time.sleep (0.5)#拟人操作
        ActionChains(self.browser).release().perform()
    def login_success(self):
        #判断是否登陆成功
        try:
            return bool(
                WebDriverWait(self.browser,5).until(
                    EC.presence_of_element_located((
                        By.XPATH,'//a[@title="消息"]'
                    ))
                )
            )
        except TimeoutException:
            return False
    def login(self):
        self.open()
        c_image,ic_image=self.get_geetest_img()
        gap=self.get_slice_gap(c_image,ic_image)
        print(f'缺口的偏移量：{gap}')
        self.drag_slider(gap-5)
        time.sleep(3)

        if self.login_success():
            print('登陆成功')
        else:
            self.login()
if __name__=='__main__':
    login=Bilibili('x','x')
    login.login()


