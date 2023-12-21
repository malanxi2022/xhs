import datetime
import os

from example.basic_usage import XhsCli
list = ["5b2707c2e8ac2b16ca3258a2", "5b3828c86b58b75e1a27b136"]
from tests.utils import beauty_print
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
cl = XhsCli.get_clinet()
# list = cl.get_user_notes(user_id="60bc119a0000000001004741")
# data = cl.get_note_by_keyword("jvm")
# beauty_print(data)
# data= cl.get_note_by_keyword("三亚", page=1, page_size=20)
# for item in data["items"]:
#     print(item)
    # print(cl.save_files_from_note_id(item["id"], dir_path="D:/xhs"))
# print(cl.get_user_info("64ca3f22000000000e024ea8"))
# list = cl.get_user_all_notes(user_id="64ca3f22000000000e024ea8")
# print(cl.save_note_by_id("657fa6e5000000003c011acf", dir_path="D:/xhs"))
# for item in list:
#     cl.save_user_all_notes(user_id=item, dir_path="D:/xhs", crawl_interval = 0)
cl.create_image_note_by_path(r"D:\xhs")
# key = ""
# download_by_search
# cl.save_search_notes(key= "三亚", dir_path="D:/xhs", crawl_interval = 0)