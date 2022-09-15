from pathlib import Path
import textwrap
import csv
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

def generate_hangtag(SKU, namaBarang, harga, brand, folderName):
    width = 350
    height = 180
    margin = 30
    offset = 20
    
    hangtag= Image.new('RGB', (width, height), color='white')
    
    nameFont = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 25)
    SKUFont = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Italic.ttf", 20)
    priceFont = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 40)
    info = ImageDraw.Draw(hangtag)
    
    for line in textwrap.wrap(namaBarang, width=25):
        info.text((margin,offset), line, font=nameFont, fill=(0,0,0))
        offset += 30
    offset += 10
    info.text((margin,offset), SKU, font=SKUFont, fill=(0,0,0))
    offset += 30
    info.text((margin,offset), harga, font=priceFont, fill=(0,0,0))
    hangtag = ImageOps.expand(hangtag, border=1, fill='grey')

    filename = SKU.replace('/', '') + '.png'
    imgPath = f'/Users/productjustika10/Desktop/hangtag_generator/{folderName}/{filename}'
    hangtag.save(imgPath)

csvFile = '/Users/productjustika10/Downloads/STARDept140922.csv'
folderName = Path(f'{csvFile}').name
folderPath = f'/Users/productjustika10/Desktop/hangtag_generator/{folderName}'
os.makedirs(folderPath)

with open(csvFile) as fileCSV:
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
            harga = row[5]
            size = row[4]
            generate_hangtag(SKU, namaBarang, harga, size, folderName)
            line += 1