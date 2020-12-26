# 测试点
# 34.132537, 108.820691
# 34.114553, 108.844761
import download
import map
if __name__ == "__main__":
    download.download(  map.LonLatSquare((108.906743, 34.237940), (108.917081, 34.227288)),
                        downloadEnerge=download.gooleMapDownload,
                        zoom=21)