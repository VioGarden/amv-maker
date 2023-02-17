import requests
import os
from conf import RUN_DIR

import time
start = time.time()


output_run_path = os.path.join(RUN_DIR, 'run3')

url_list = []
url_list.append(("https://files.catbox.moe/3d9bbl.webm", "kaze"))
url_list.append(("https://files.catbox.moe/9xdp21.webm", "chainsaw_man"))
url_list.append(("https://files.catbox.moe/p2ievv.webm", "kimi_no_na_wa"))



for url in url_list:
    response = requests.get(url[0])
    with open(os.path.join(output_run_path, f"{url[1]}.mp4"), "wb") as f:
        f.write(response.content)

print(time.time() - start)