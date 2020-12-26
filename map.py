import math
# 瓦片
class Tail():
    pass

# 正方形坐标
class LonLatSquare():
    
    def __init__(self, p1, p2) -> None:
        self.x1 = p1[0]
        self.x2 = p2[0]
        self.y1 = p1[1]
        self.y2 = p2[1]
    def __str__(self) -> str:
        return "LonLatSquare:\t({}, {}), ({}, {})".format(self.x1, self.y1, self.x2, self.y2)
    
    def getP1(self):
        return (self.x1, self.y1)
    def getP2(self):
        return (self.x2, self.y2)

class Trans(object):

    @staticmethod
    def LonLat2TailGoogle(lon, lat, zoom):
        n = math.pow(2, zoom);
        tilex = ((lon + 180) / 360) * n;
        tiley = (1 - (math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))) / math.pi)) / 2 * n;
        x = int(math.floor(tilex))
        y = int(math.floor(tiley))
        return (x, y)
if __name__ == "__main__":
    rs = Trans.LonLat2TailGoogle(108.820691, 34.132537,  16)
    print(rs)
