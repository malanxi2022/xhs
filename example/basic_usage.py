import datetime
import json
from time import sleep
from xhs import XhsClient, DataFetchError, help
from playwright.sync_api import sync_playwright


def sign(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = r"D:\docker\xhs\stealth.min.js"
                chromium = playwright.chromium

                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                browser = chromium.launch(headless=True)

                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                # 这个地方设置完浏览器 cookie 之后，如果这儿不 sleep 一下签名获取就失败了，如果经常失败请设置长一点试试
                sleep(1)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception:
            # 这儿有时会出现 window._webmsxyw is not a function 或未知跳转错误，因此加一个失败重试趴
            pass
    raise Exception("重试了这么多次还是无法签名成功，寄寄寄")

class XhsCli():

    @staticmethod
    def get_clinet():
        cookie = "1a1=18899128b85l5n8twc100c9axk1spz7kx7ki6j47f50000247056; webId=15840f0fd45c7d6368c7ee14b82e26cf; gid=yYYjjyJYj2CKyYYjjyJYDWV4Y212IY9ESy88TWiSj0CTy328MUuWTK888J4W82K8qYKJ4W2f; gid.sign=0bbbu1JE19T6P9g0+QaoPEwa61M=; abRequestId=15840f0fd45c7d6368c7ee14b82e26cf; webBuild=3.20.3; xsecappid=xhs-pc-web; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=4c563fe5-d635-4be9-a887-46c649e4e9ef; unread={%22ub%22:%22656d3008000000000901e421%22%2C%22ue%22:%22656e611800000000090203ea%22%2C%22uc%22:29}; web_session=040069b5f50f250114520c2bb4374bec758255; cacheId=f6855de5-876a-4091-ad69-ed9fc0ac9e82"
        return XhsClient(cookie, sign=sign)
