#导入依赖库
import os
from agentocr import OCRSystem  #OCR识别的主要库
import fitz                            #PDF转图片库
from PIL import Image
import shutil
#获取文件

def get_filename(path):
    file_list=[]
    for root,dirs,files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root,file))
    return file_list

#PDF转图片

def pyMuPDF_fitz(pdfPath, imagePath):
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为4，这将为我们生成分辨率提高4的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 4  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 4
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建
        try:
            pix.writePNG(imagePath + '/' + os.path.split(pdfPath)[1][:-4]+'.png')  # 将图片写入指定的文件夹内
        except Exception as e:
            print(e)



#OCR识别

# 通过 config 参数来进行模型配置，内置多国语言的配置文件
def ocr_2_txt(file):
    line_list=[]
    ocr = OCRSystem(config='ch')
    result = ocr.ocr(file)
    name = os.path.split(file)[1][:-4]
    for line in result:
        string = line[1][0]
        with open(os.path.split(file)[0]+'/'+'{}.txt'.format(name),'a',encoding='utf8') as f:
            f.write(string + '\n')
##切割长图
def splitimage(src, dstpath):
    os.chdir(dstpath)
    img = Image.open(src)
    w, h = img.size
   
    height=w*297/210 #A4纸比例出的高度
    num=h/height+1#将分割出的图片数量
    index=0
   
    s = os.path.split(src)#分割出路径和文件名
    if dstpath == '':
        dstpath = s[0]
    fn = s[1].split('.')
    basename = fn[0]#文件名
    postfix = fn[-1]#后缀名    
    while (index < num):
        box = (0, height-1527, w, height)
        if not os.path.exists(basename):  # 判断存放图片的文件夹是否存在
            os.makedirs(basename)
        try:
            img.crop(box).save(os.path.join(os.path.join(dstpath,basename), basename + '_' + str(index) + '.' + postfix), img.format)
            height = height + 1527
            index = index + 1            
        except Exception as e:
            print(e)
            continue       
##合并内容
def merge_txt(path):
    name = path.split('/')[-1]
    file_list = get_filename(path)
    file_list.sort(key=lambda x: int(x.split('_')[1][:-4]))
    text_list = []
    for file_one in file_list:
        if file_one.endswith('txt'):
            with open(file_one,'r',encoding='utf8') as f:
                text = f.read()
                text_list.append(text)
    with open('{}.txt'.format(name),'a',encoding='utf8')as g:
       
        g.write(','.join(text_list))
        
    

if __name__ == '__main__':
    dirpath = r'D:\chengkang\个人\股票'
    files = get_filename(dirpath)
    for file in files:
        if file.endswith('pdf'):
            pyMuPDF_fitz(file,dirpath)
            allfile = get_filename(dirpath)
            for one in allfile:
                if one.endswith('png'):
                    img = Image.open(one)
                    w, h = img.size
                    if h > 1000:
                        splitimage(one,os.path.split(one)[0])
                        splitfiles = get_filename(one.split('.')[0])
                        for spfile in splitfiles:
                            ocr_2_txt(spfile)
                        merge_txt(dirpath + '/' +os.path.split(one)[1].split('.')[0])
                        shutil.rmtree(dirpath + '/' +os.path.split(one)[1].split('.')[0])
                    else:
                        ocr_2_txt(one)
        elif file.endswith('png'):
            img = Image.open(file)
            w, h = img.size
            if h > 1000:
                splitimage(file,os.path.split(file)[0])
                splitfiles = get_filename(file.split('.')[0])
                for spfile in splitfiles:
                    ocr_2_txt(spfile)
                merge_txt(dirpath + '/' +os.path.split(file)[1].split('.')[0])
                shutil.rmtree(dirpath + '/' +os.path.split(file)[1].split('.')[0])
            else:
                ocr_2_txt(file)
    print('完成')
