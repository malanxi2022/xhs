import datetime
import os

from xhs import SearchSortType

from example.basic_usage import XhsCli
list = ["5b2707c2e8ac2b16ca3258a2", "5d247905000000001201aaba", "5b89698af2a6c5000118e087"]
from tests.utils import beauty_print
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
cl = XhsCli.get_clinet()

# print(cl.get_user_all_note_ids("5b3828c86b58b75e1a27b136"))
data = cl.get_note_by_keyword(keyword="", sort=SearchSortType.LATEST)
for item in data["items"]:
    note_id = item["id"]
    user_id = item["note_card"]["user"]["user_id"]
    cl.comment_note(note_id, "06 ")
    # cl.like_note(note_id)
    # break