from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
import qrcode
import textwrap
import csv
import os
from pathlib import Path

def generate_barcode(SKU):
    barcode = Code128(SKU, writer=ImageWriter())
    options = {
        'module_height':7,
        'font_size':6,
        'text_distance':3,
        'quiet_zone': 0
    }
    barcode.save("barcode", options)

def generate_qr(SKU):
    qrPref = qrcode.QRCode(
        box_size=6,
        border=0
    )
    qrPref.add_data(SKU)
    qrPref.make()
    qr = qrPref.make_image()
    qr.save('qrcode.png')


def generate_hangtag(SKU, namaBarang, harga, brand, folderName):
    width = 590
    height = 354
    margin = 30
    offset = 20
    
    hangtag= Image.new('RGB', (width, height), color='white')
    
    nameFont = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 25)
    priceFont = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 40)
    info = ImageDraw.Draw(hangtag)
    
    info.text((margin,offset), brand, font=nameFont, fill=(0,0,0))
    offset += 10
    for line in textwrap.wrap(namaBarang, width=25):
        offset += 30
        info.text((margin,offset), line, font=nameFont, fill=(0,0,0))
    offset += 40
    info.text((margin,offset), harga, font=priceFont, fill=(0,0,0))

    generate_barcode(SKU)
    barcodeImg = Image.open('barcode.png')
    middle = int((width / 2) - (barcodeImg.width / 2))
    bottommost = height-barcodeImg.height
    hangtag.paste(barcodeImg, (middle, bottommost))

    generate_qr(SKU)
    qrImg = Image.open('qrcode.png')
    rightmost = width-margin-qrImg.width
    hangtag.paste(qrImg, (rightmost, 20))
    
    filename = SKU.replace('/', '') + '.png'
    imgPath = f'/Users/productjustika10/Desktop/hangtag_generator/{folderName}/{filename}'
    hangtag.save(imgPath)

a4 = Image.new('RGB', (3508, 2480), color='white')

# def add_to_a4(img, qty):
#     x = 60
#     y = 60
    
#     for i in range(qty-1):
#         a4.paste(img, )




folderName = Path(f'/Users/productjustika10/Downloads/Stok baju - Copy of Sheet1 (3).csv').name
folderPath = f'/Users/productjustika10/Desktop/hangtag_generator/{folderName}'
os.makedirs(folderPath)

with open('/Users/productjustika10/Downloads/Stok baju - Copy of Sheet1 (3).csv') as fileCSV:
    data = csv.reader(fileCSV, delimiter=";")

    line = 1
    for row in data:
        if '' in row:
            errorMsg = 'Data tidak lengkap di row ' + str(line)
            print(errorMsg)
            line += 1
        else:
            SKU = row[1]
            namaBarang = row[2]
            harga = row[4]
            brand = row[0]
            generate_hangtag(SKU, namaBarang, harga, brand, folderName)
            line += 1

# dirs = os.listdir('/Users/productjustika10/Desktop/hangtag_generator/Stok baju - Copy of Sheet1 (3).csv')
# for file in dirs:
#     print(file)