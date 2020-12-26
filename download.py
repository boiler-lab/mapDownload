import requests
import config
import map
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import cv2
import numpy as np
import tqdm
'''
description: 下载地图瓦片
param {*}:  url: 下载地址
            savePath: 保存地址
return {*}: Boolean: 是否下载成功
'''
def downloadTile(url, savePath, t):
    if(config.proxy == True):
        res = requests.get(url, proxies = config.proxies)
    else:
        res = requests.get(url)
    if(res.status_code == 200):
        with open(savePath, 'wb') as f:
            f.write(res.content)
            imagebuff = np.asarray(bytearray(res.content), dtype="uint8")
            image = cv2.imdecode(imagebuff, cv2.IMREAD_COLOR)
            t.update(1)
            return image
    else:
        print("error" + res.status_code)
    

def gooleMapDownload(lonLatSquare, zoom):
    print("==================google map download==================================")
    (x1, y1) = map.Trans.LonLat2TailGoogle(lonLatSquare.getP1()[0], lonLatSquare.getP1()[1], zoom=zoom)
    (x2, y2) = map.Trans.LonLat2TailGoogle(lonLatSquare.getP2()[0], lonLatSquare.getP2()[1], zoom=zoom)
    print("({}, {}), ({}, {}), lenx:{}, leny:{}, sum:{}".format(x1, y1, x2, y2, x2-x1+1, y2-y1+1, ( (x2-x1+1)* (y2-y1+1))))
    lenx = x2-x1+1
    leny = y2-y1+1
    futures = []
    pool = ThreadPoolExecutor(100)
    print("download")
    pbar = tqdm.tqdm(total=lenx*leny)
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            url = "https://khms0.google.com/kh/v=883?x={}&y={}&z={}".format(x, y, zoom)
            futures.append(pool.submit(downloadTile, url, "./google/{}_{}_{}.jpg".format(x, y, zoom), pbar))
            #downloadTile(url=url, savePath="./google/{}_{}_{}.jpg".format(x, y, zoom))
    
    wait(futures, return_when=FIRST_COMPLETED)
    print("over")
    images = [f.result() for f in futures]
    pbar.close()
    # 拼接
    print("concat")
    himage = []
    for y in tqdm.trange(leny):
        h = images[y*lenx: y*lenx+lenx]
        himage.append(cv2.hconcat(h))
    allimage = cv2.vconcat(himage)
    cv2.imwrite("./download/all_{}.jpg".format(zoom), allimage)
    

def download(lonLatSquare, downloadEnerge, zoom):
    print(lonLatSquare)
    downloadEnerge(lonLatSquare, zoom)

    
if __name__ == "__main__":
    url = "https://khms0.google.com/kh/v=883?x=52600&y=26125&z=16"
    downloadTile(url, "./test.jpg")