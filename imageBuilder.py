from PIL import Image, ImageDraw, ImageFont

class ImageBuilder:
    def __init__(self, length):
        self.full_img = Image.new('RGB', (length, 16), color = (0,0,0))

        self.fnt = ImageFont.truetype('arial.ttf', 12)

        self.xCoord = 0


    def addImage(self,txt, rgb):
        img = Image.new('RGB',((len(txt) * 7), 16), color =( 0,0,0))
        d = ImageDraw.Draw(img)
        d.text((0,0), txt, font = self.fnt, fill = rgb)

        self.full_img.paste(img, (self.xCoord, 0))
        self.xCoord += img.size[0]

    def saveImage(self):

        self.full_img.save('imageToPrint.png')