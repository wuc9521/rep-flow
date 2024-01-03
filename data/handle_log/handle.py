import os
import re
import glob
import imagehash
from PIL import Image, ImageDraw

def get_coord_from_log(log_file, image_name):
    with open(log_file) as f:
        for line in f:
            if f'{image_name}.png' in line:
                x = re.search(r'\((\d+.\d+),', line).group(1)
                y = re.search(r',\s*(\d+.\d+)\)', line).group(1)
                return float(x), float(y)

def add_circle(image_path, x, y, radius=20):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline='red')
    image.save(image_path)
    
def deduplicate(image_folder, hash_thresh=5):
    hashes = {}
    for image_path in glob.glob(os.path.join(image_folder, '*.png')):
        hash = imagehash.average_hash(Image.open(image_path))
        if hash in hashes:
            os.remove(image_path)
        else:
            for key in hashes:
                if abs(hash - key) <= hash_thresh:
                    os.remove(image_path)
                    break
            else:
                hashes[hash] = image_path
            
def find_start_end(image_folder):
    home_image = Image.open('home.png')
    home_hash = imagehash.average_hash(home_image)
    
    start_image = None
    end_image = None
    
    for image_path in glob.glob(os.path.join(image_folder, '*.png')):
        hash = imagehash.average_hash(Image.open(image_path))
        if hash == home_hash:
            if not start_image:
                start_image = image_path
            else:
                end_image = image_path
                break
                
    return start_image, end_image

def get_line_number(log_lines, image_path):
    image_name = os.path.basename(image_path)
    for i, line in enumerate(log_lines):
        if image_name in line:
            return i
    return -1
    
def main(log_file, image_folder):
    deduplicate(image_folder)
    
    for image_path in glob.glob(os.path.join(image_folder, '*.png')):
        x, y = get_coord_from_log(log_file, image_path)
        add_circle(image_path, x, y)
        
    start, end = find_start_end(image_folder)
    
    with open(log_file) as f:
        lines = f.readlines()
        start_line = get_line_number(lines, start)
        end_line = get_line_number(lines, end)
        
        for i in range(start_line, end_line+1):
            print(lines[i].strip())
            
main('../../test/log/monkey.log', '../guidance/1')