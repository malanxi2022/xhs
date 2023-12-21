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

class XhsCliMA():

    @staticmethod
    def get_clinet():
        cookie = "a1=18c8bd11e38qpzzgmdnfjssvqtsehi1p0i156infz50000395480; webId=30824e869da08c6274c585713b4319f2; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=b876ce47-a871-4ba9-ad8a-91d0d5db79ac; gid=yYSYDfyyij8WyYSYDfyyd33IqYAUuuk6fIiVyiuMMhA9M228dx3yUK888qj24Y88y4qDYKqy; abRequestId=30824e869da08c6274c585713b4319f2; webBuild=3.21.1; xsecappid=xhs-pc-web; web_session=040069b3715a7c5bc860ad44b1374bb3884b1b; unread={%22ub%22:%22658065020000000006023985%22%2C%22ue%22:%226583aa5c000000003801ff36%22%2C%22uc%22:29}"
        return XhsClient(cookie, sign=sign)
