import numpy as np
from PIL import Image,ImageOps,ImageFilter
import pytesseract

def fillup_gap(ar,i):
    direction = ((-1,1),(1,1),(1,0))
    for j in range(1,len(ar[0])-1):
        possible = False
        for k in direction:
            if ar[i+k[0]][j+k[1]] == 0 and ar[i-k[0]][j-k[1]]==0:
                possible = True
                break
        if possible:
            ar[i][j]=0

def white_black(fi):
    ar = np.array(fi)
    w = np.sum(ar==255)
    b = np.sum(ar==0)
    return w,b

def solve_black_dots(x,y,ar):
    perm = (0,1,-1)
    tot = 0
    for i in perm:
        for j in perm:
            tot+=ar[x+i][y+j]
    if tot == 8*255:
        ar[x][y]=255

def remove_black_dots(fi):
    ar = np.array(fi)
    ar[0,0:len(ar[0])] = 255
    ar[len(ar)-1,0:len(ar[0])] = 255
    ar[0:len(ar),0] = 255
    ar[0:len(ar),len(ar[0])-1] = 255
    for x in range(1,len(ar)-1):
        for y in range(1,len(ar[0])-1):
            if ar[x][y]==0:
                solve_black_dots(x,y,ar)
    return ar

def clear_n_get_text(filename):
    fi = Image.open(filename)
    gray = ImageOps.grayscale(fi)
    w,b = white_black(gray)
    if w<b:
        gray = ImageOps.invert(gray)
    ar = remove_black_dots(gray)
    fillup_gap(ar,8)
    out = Image.fromarray(ar)
    text = pytesseract.image_to_string(out,lang='captcha')[:6] #use lang to captcha if you use my trained data
    modification = text.replace("S","5").replace("E","6").replace("O","0")
    return modification