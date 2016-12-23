from PIL import Image
import pymysql

im = Image.open("capcha.gif")
im = im.convert("P")


print(im.size)
"a".format