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
        cookie = "1abRequestId=3ecafc7f-67ab-5722-b865-74fcf277f25e; webBuild=3.20.3; xsecappid=xhs-pc-web; a1=18c8697c15dok0bjvyk0yxutvkneq34dlzd95hojd50000311063; webId=444a29365e2641038f2951f6faf9eaf5; websectiga=cf46039d1971c7b9a650d87269f31ac8fe3bf71d61ebf9d9a0a87efb414b816c; sec_poison_id=ec33d1d0-1700-4ae5-87d5-a4a7565f69fd; gid=yYSYKjWSKj14yYSYKjWSyuxl2flT8DVhvT8vfVfC79hTIj28dAq4f2888qyy8Kq82diiYiyY; web_session=040069b17f4ac356eb4827feb7374bc0b97946; unread={%22ub%22:%22658178e6000000000700a55e%22%2C%22ue%22:%2265816ac200000000060283ff%22%2C%22uc%22:22}"
        return XhsClient(cookie, sign=sign)
