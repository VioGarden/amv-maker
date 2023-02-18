import requests
import os
from conf import RUN_DIR

import time
start = time.time()


output_run_path = os.path.join(RUN_DIR, 'run1')

url_list = []
url_list.append(("https://files.catbox.moe/cdf1hm.webm", "attack_on_titan"))
url_list.append(("https://files.catbox.moe/c7wtd4.webm", "spy_x_family"))
url_list.append(("https://files.catbox.moe/ef2ntg.webm", "demon_slayer"))
url_list.append(("https://files.catbox.moe/hfybji.webm", "fate_ubw"))
# url_list.append(("https://files.catbox.moe/p5bjvw.webm", "one_punch_man"))
# url_list.append(("https://files.catbox.moe/ya38xy.webm", "bungo_stray_dogs"))
# url_list.append(("https://files.catbox.moe/2f4860.webm", "haikyu"))
# url_list.append(("https://files.catbox.moe/dcu52b.webm", "re_creators"))

for url in url_list:
    response = requests.get(url[0])
    with open(os.path.join(output_run_path, f"{url[1]}.mp4"), "wb") as f:
        f.write(response.content)

print(time.time() - start)