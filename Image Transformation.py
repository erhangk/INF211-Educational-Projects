import random

def generate_random(row,column):
    gen_list=[]
    dict1={}
    for i in range(row):
        empty_list=[]
        for x in range(column):
            dict1["red"]=random.randint(0,255)
            dict1["green"]=random.randint(0,255)
            dict1["blue"]=random.randint(0,255)
            empty_list.append(dict1)
            dict1={}
        gen_list.append(empty_list)
    return gen_list

def is_valid(img):
    for i in img:
        for x in i:
            for l in x.values():
                if isinstance(l,(int)) and 0<=l<=255:
                    continue
                else: 
                    print(l)
                    return False
    return True

def read_from_file(filename):
    f=open(filename,"r")
    l1=[]
    d1={}
    temp_list=[]
    for i in f:
        x=i.strip()
        for l in x.split(","):
            d1["red"]=int(l[0:2],16)
            d1["green"]=int(l[2:4],16)
            d1["blue"]=int(l[4:6],16)
            temp_list.append(d1)
            d1={}
        l1.append(temp_list)
        temp_list=[]
    f.close()
    return l1
        
def write_to_file(img,filename):
    f=open(filename,"w")
    line=""
    temp_line=""
    for i in img:
        for x in i:
            temp_line+=hex(x["red"])[2:]
            temp_line+=hex(x["green"])[2:]
            temp_line+=hex(x["blue"])[2:]
            temp_line+=","
            line+=temp_line
            temp_line=""
        line=line[:-1]+"\n"
        f.write(line)
        line=""

def clear(img):
    for i in img:
        for x in i:
            x["red"],x["green"],x["blue"]=0,0,0
    return img

def set_value(img, value, channel='rgb'):
    for i in img:
        for x in i:
            for l in channel:
                if l=="r":
                    x["red"]=value
                elif l=="g":
                    x["green"]=value
                elif l=="b":
                    x["blue"]=value
    fix(img)
    
def fix(img):
    for i in img:
        for x in i:
            for key in x.keys():
                if x[key]>255:
                    x[key]=255
                elif x[key]<0:
                    x[key]=0
                elif not isinstance(x[key],int):
                    x[key]=round(x[key])

def rotate90(img):
    img_new=img.copy()
    img_new.reverse()
    l1=[]
    temp=[]
    for j in range(len(img[0])):
        for i in img_new:
            temp.append(i[j])
        l1.append(temp)
        temp=[]
    return l1
                
def rotate180(img):
    img_new=rotate90(rotate90(img))
    return img_new

def rotate270(img):
    img_new=rotate90(rotate90(rotate90(img)))
    return img_new
    
def mirror_x(img):
    for i in img:
        i.reverse()
    
def mirror_y(img):
    img.reverse()
    
def enhance(img, value, channel='rgb'):
    for i in img:
        for x in i:
            for l in channel:
                if l=="r":
                    x["red"]=x["red"]*value
                elif l=="g":
                    x["green"]=x["green"]*value
                elif l=="b": 
                    x["blue"]=x["blue"]*value
    fix(img)


def grayscale(img,mode=1):
    for i in img:
        for x in i:
            if mode==1:
                values=x.values()
                weighted_a=round(sum(values)/3)
                x["red"],x["green"],x["blue"]=weighted_a,weighted_a,weighted_a
            elif mode==2:
                a=x["red"]* 0.299 + 0.587*x["green"]+0.114* x["blue"]
                x["red"],x["green"],x["blue"]=a,a,a
            elif mode==3:
                a=x["red"]*0.2126+ 0.7152* x["green"]+ 0.0722* x["blue"]
                x["red"],x["green"],x["blue"]=a,a,a
            elif mode==4:
                a=x["red"]*0.2627+ + 0.6780 * x["green"]+0.0593 * x["blue"]
                x["red"],x["green"],x["blue"]=a,a,a
    fix(img)


def get_freq(img, channel='rgb', bin_size=16):
    bins={"bin_size":bin_size}
    if "r" in channel: bins["red"]=[0 for i in range(int(256/bin_size))]
    if "g" in channel: bins["green"]=[0 for i in range(int(256/bin_size))]
    if "b" in channel: bins["blue"]=[0 for i in range(int(256/bin_size))]
    ranges=[]
    n=0
    for i in range(int(256/bin_size)):
        ranges.append(list(range(256))[n: n+bin_size])
        n+=bin_size
    for i in img:
        for x in i:
            for l in ranges:
                if x["red"] in l and "r" in channel:
                    bins["red"][ranges.index(l)]+=1
                elif x["green"] in l and "g" in channel:
                    bins["green"][ranges.index(l)]+=1
                elif x["blue"] in l and "b" in channel:
                    bins["blue"][ranges.index(l)]+=1
    return bins

def scale_down(img, N):
    avg_r=0
    avg_g=0
    avg_b=0
    img_copy=[]
    for i in img:
        img_copy.append(i.copy())
    rpt=N**2
    newimg=[]
    while len(img_copy)%N!=0:
        img_copy.append(img_copy[-1])
    while len(img_copy[-1])%N!=0:
        for i in img_copy:
            i.append(i[-1])
            if len(img_copy[-1])%N==0:
                break
    row=len(img_copy)
    column=len(img_copy[0])
    for i in range(0, row, N):
        newimg.append([])
        for m in range(0, column, N):
            for j in range(N-1):
                for t in range(N-1):
                    avg_r+=img_copy[i+j][m+t]["red"] 
                    avg_g += img_copy[i+j][m+t]["green"] 
                    avg_b += img_copy[i+j][m+t]["blue"]
            avg_r=avg_r/rpt
            avg_g=avg_g/rpt
            avg_b=avg_b/rpt
            newimg[-1].append({"red":avg_r, "green":avg_g , "blue":avg_b})
            avg_r=0
            avg_g=0
            avg_b=0
    fix(newimg)
    return newimg
print(scale_down([[{'red': 244, 'green': 122, 'blue': 24}, {'red': 157, 'green': 91, 'blue': 36}, {'red': 154, 'green': 206, 'blue': 168}, {'red': 153, 'green': 212, 'blue': 55}, {'red': 50, 'green': 246, 'blue': 242}], [{'red': 172, 'green': 175, 'blue': 63}, {'red': 245, 'green': 59, 'blue': 254}, {'red': 218, 'green': 19, 'blue': 154}, {'red': 171, 'green': 79, 'blue': 85}, {'red': 192, 'green': 44, 'blue': 33}], [{'red': 43, 'green': 101, 'blue': 113}, {'red': 31, 'green': 197, 'blue': 4}, {'red': 50, 'green': 201, 'blue': 148}, {'red': 229, 'green': 250, 'blue': 111}, {'red': 216, 'green': 42, 'blue': 188}], [{'red': 112, 'green': 133, 'blue': 85}, {'red': 220, 'green': 98, 'blue': 183}, {'red': 58, 'green': 32, 'blue': 14}, {'red': 231, 'green': 103, 'blue': 60}, {'red': 254, 'green': 203, 'blue': 131}], [{'red': 106, 'green': 21, 'blue': 110}, {'red': 74, 'green': 53, 'blue': 101}, {'red': 234, 'green': 193, 'blue': 185}, {'red': 77, 'green': 53, 'blue': 249}, {'red': 75, 'green': 207, 'blue': 216}]],1))

def scale_up(img, N):
    new_img=[]
    temp_list=[]
    for i in img:
        for x in i:
            for l in range(N):
                temp_list.append(x)
        for j in range(N):
            new_img.append(temp_list)
        temp_list=[]
    return new_img
        
def apply_window(img, window):
    img_copy=[]
    out=[]
    x=1
    y=1
    avg=[0,0,0]
    for i in img:
        img_copy.append(i.copy())
    for i in range(len(img_copy)):
        img_copy[i].append(img_copy[i][-1])
        img_copy[i].insert(0, img_copy[i][0])
    img_copy.append(img_copy[-1])
    img_copy.insert(0, img_copy[0])
    for i in img_copy:
        out.append([])
        for j in i:
            for t in range(0, 3):
                for n in range(0, 3):
                    if x>=len(img_copy[0])-1:
                        break
                    avg[0]+=img_copy[y-(1-t)][x-(1-n)]["red"]*window[t][n]
                    avg[1]+=img_copy[y-(1-t)][x-(1-n)]["green"]*window[t][n]
                    avg[2]+=img_copy[y-(1-t)][x-(1-n)]["blue"]*window[t][n]
    
            x+=1
            if x<=len(img_copy[0])-1:
                out[-1].append({"red":avg[0], "green":avg[1], "blue":avg[2]})
            avg=[0,0,0]
        if y>=len(img_copy)-2:
            break
        y+=1
        x=1
    fix(out)
    return out 