import cv2 
import os 
from pathlib import Path
import shutil 
import random
import numpy as np 


def rotate_img(img,angle_value:int):
    angle_pos = angle_value
    angle_neg = -angle_value
    angle = random.choice([angle_pos,angle_neg])
    height,width = img.shape[:2]

    center = (width//2,height//2)

    rotation_mat = cv2.getRotationMatrix2D(center=center,angle=angle,scale=1.0)

    rotated_img = cv2.warpAffine(img,rotation_mat,dsize=(width,height),borderValue=(255,255,255))

    return rotated_img

def grayscale_conversion(img):
    
    grayscaled_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    return grayscaled_img

def add_blur(img,sigma_x=0.6,sigma_y=0.6): #sigma_x and sigma_y control the blur intensity

    blurred_img = cv2.GaussianBlur(img,(3,3),sigma_x,sigma_y)

    return blurred_img

def add_color_jitter(img):

    alpha_factor = round(random.uniform(0.5,1.5),1)
    adjusted_img = cv2.convertScaleAbs(img,alpha=alpha_factor)
    
    hsv_image = cv2.cvtColor(adjusted_img,cv2.COLOR_BGR2HSV)

    hue_factor = random.randint(-50,50)
    saturation_factor = round(random.uniform(0.5,1.5),1)
    brightness_factor = random.randint(-50,50)


    # Adjust hue
    hsv_image[:,:,0] = (hsv_image[:,:,0] + hue_factor) % 180  # hue values are in range 0-180

    # Adjust saturation
    hsv_image[:,:,1] = np.clip(hsv_image[:,:,1] * saturation_factor, 0, 255)

    # Adjust brightness
    hsv_image[:,:,2] = np.clip(hsv_image[:,:,2] + brightness_factor, 0, 255)

    # Convert back to BGR
    hsv_adjusted = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return hsv_adjusted


def augment_image(img):
    rotated_img_10 = rotate_img(img,10)
    rotated_img_20 = rotate_img(img,20)
    grayscaled_img = grayscale_conversion(img)
    blurred_img = add_blur(img)
    jittered_img = add_color_jitter(img)
    transformed_images = [rotated_img_10,rotated_img_20,grayscaled_img,
                          blurred_img,jittered_img]
    return transformed_images

source_directory = Path('/home/pujan/D/datasets/nepali_modified/nhcd')

for class_directory in source_directory.iterdir():
    if class_directory.is_dir():
        images_path = list(class_directory.glob("**/*.jpg"))
        for i,single_image_path in enumerate(images_path):
            img = cv2.imread(str(single_image_path))
            transformed_images = augment_image(img)
            os.chdir(class_directory)
            for j,trans_img in enumerate(transformed_images):
                orig_file_name = os.path.basename(single_image_path)
                augment_file_name = f"{j}aug{orig_file_name}"
                cv2.imwrite(augment_file_name,trans_img)
            

