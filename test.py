# Image allows for open, save, show of images
# ImageDraw allows editting of image
# ImageFont allows choice of font
from PIL import Image, ImageDraw, ImageFont

# assign variable name and open image
NFT = Image.open('default.png')

# convert image into editable form
edit = ImageDraw.Draw(NFT)

# Font selection
myFont = ImageFont.truetype('MISTRAL.TTF', 55)

edit.text((225, 30), "Kassie's KupKakes", fill =(255, 0, 0), font=myFont)
edit.text((225, 153), "Kassie Overton", fill =(255, 0, 0), font=myFont)

# show and save the image

NFT.show()
NFT.save('business_NFT.png')