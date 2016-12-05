import sys
import os
from PIL import Image, ImageEnhance

class ImgHelper:
    def __init__(self):
        pass

    def save(self, im, imgSrc, imgTgt, imgNameNew, q=90):
        imgSrc = os.path.split(imgSrc)[1]
        if not os.path.exists(imgTgt) : os.makedirs(imgTgt)
        im.save(imgTgt + '\\' + imgSrc.split('.')[0] + imgNameNew +'.jpg', quality=q)
       
    def ratio(self, imgpath, width=600):
        im = Image.open( imgpath )
        (srcWidth, srcHeight) = im.size
        height = int(float(width)/float(srcWidth)*float(srcHeight))
        im.thumbnail( (width,height) )
        return im
   
    def reduceOpacity(self, im, opacity): 
        """Returns an image with reduced opacity.""" 
        assert opacity >= 0 and opacity <= 1 
        if im.mode != 'RGBA': 
            im = im.convert('RGBA') 
        else: 
            im = im.copy() 
        alpha = im.split()[3] 
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity) 
        im.putalpha(alpha) 
        return im 
     
    def watermark(self, imagefile, markfile, sw=0, sh=0, opacity=1): 
        """Adds a watermark to an image."""     
        im = Image.open(imagefile) 
        mark = Image.open(markfile)     
        if opacity < 1: 
            mark = self.reduceOpacity(mark, opacity) 
        if im.mode != 'RGBA': 
            im = im.convert('RGBA') 
        # create a transparent layer the size of the image and draw the 
        # watermark in that layer. 
        layer = Image.new('RGBA', im.size, (0,0,0,0))
       
        if sw<0: sw = im.size[0] - mark.size[0] + sw
        if sh<0: sh = im.size[1] - mark.size[1] + sh
        position = (sw, sh)
        layer.paste(mark, position)
       
        # composite the watermark with the layer 
        return Image.composite(layer, im, layer)
    
    # 将水印填充整个图片
    def watermarkfull(self, dstfile, imagefile, markfile, smallmarkfile, opacity=1):
        '''
        将水印填充整个图片
        '''
        im = Image.open(imagefile) 
        
        mark = Image.open(markfile)
        if im.size[0]<mark.size[0] or im.size[1]<mark.size[1]:
            mark = Image.open(smallmarkfile)
        if im.size[0]<mark.size[0] or im.size[1]<mark.size[1]:
            # 文字水印
            return None
            
        if opacity < 1: 
            mark = self.reduceOpacity(mark, opacity) 
        if im.mode != 'RGBA': 
            im = im.convert('RGBA') 
        # create a transparent layer the size of the image and draw the 
        # watermark in that layer. 
        layer = Image.new('RGBA', im.size, (0,0,0,0))
        sw = 0
        sh = 0
        while sh+mark.size[1]<im.size[1]:
            sw = 0
            while sw + mark.size[0]<im.size[0]:
                position = (sw, sh)
                layer.paste(mark, position)
                sw = sw + mark.size[0]
            sh = sh + mark.size[1]
        
        # composite the watermark with the layer 
        return Image.composite(layer, im, layer).save(dstfile, quality=90)
    
if __name__=='__main__':
    ih = ImgHelper()
    im = ih.watermarkfull('2.jpg','www.ichinachess.com\\0001\\2016111013530952497.jpg', 'www.ichinachess.com.png',None, 0.3)
    