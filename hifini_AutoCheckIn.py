import time
import random
import requests
import schedule
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# 配置信息
LOGIN_URL = "https://www.hifini.com/user-login.htm"
SIGN_URL = "https://www.hifini.com/sg_sign.htm"
USERNAME = "1403509868@qq.com"
PASSWORD = "a887568500"

# **设置 Chrome 浏览器**
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 让浏览器不自动关闭
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# **登录函数**
def login():
    driver.get(LOGIN_URL)
    time.sleep(2)

    # 输入账号
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys(USERNAME)

    # 输入密码
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(PASSWORD)

    # 让用户手动拖动滑块验证码
    input("请手动完成验证码后，按 Enter 继续...")

    # 点击登录
    login_button = driver.find_element(By.CLASS_NAME, "btn-login")
    login_button.click()

    time.sleep(5)  # 等待页面跳转

    # **获取 Cookie**
    cookies = driver.get_cookies()
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    print(f"获取到的 Cookie: {cookie_str}")
    return cookie_str

# **签到函数**
def sign_in(cookie_str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.hifini.com/",
        "Cookie": cookie_str
    }
    session = requests.Session()
    response = session.get(SIGN_URL, headers=headers)

    if "签到成功" in response.text:
        print(f"{datetime.now()} - 签到成功")
    else:
        print(f"{datetime.now()} - 签到失败，可能是已签到或请求错误")

# **每日随机签到**
def schedule_random_sign_in():
    hour = random.randint(6, 23)
    minute = random.randint(0, 59)
    sign_time = f"{hour}:{minute}"
    print(f"今天的签到时间为 {sign_time}")

    schedule.every().day.at(sign_time).do(lambda: sign_in(cookie_str))

# **主程序**
cookie_str = login()  # 先登录，获取 Cookie
schedule_random_sign_in()  # 设定每日签到时间

# **持续运行**
while True:
    schedule.run_pending()
    time.sleep(30)
