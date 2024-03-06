import torch 
import cv2 
from torchvision.transforms import v2
from torchvision import transforms
import numpy as np 

img_transforms = v2.Compose([
    transforms.ToTensor(),
    v2.ToDtype(torch.float32),
    v2.Normalize((0.5,),(0.5,))
])

def crop_characters(img) -> np.array:


    blur_img =cv2.GaussianBlur(img,(5,5),3)
    gray = cv2.cvtColor(blur_img,cv2.COLOR_BGR2GRAY)

    # bin_img= cv2.threshold(gray,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    thres_value,thresh_img= cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(img,contours,-1,(0,255,0),2)


    bounding_boxes = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area<200:
            continue
        # Get the bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)
        
        # Draw rectangle around contour
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0),1)
        
        # Store bounding box coordinates
        bounding_boxes.append((x, y, x + w, y + h))

    # Calculate the minimum bounding rectangle that encloses all the smaller bounding rectangles
    x_min = min(box[0] for box in bounding_boxes) 
    y_min = min(box[1] for box in bounding_boxes)
    x_max = max(box[2] for box in bounding_boxes)
    y_max = max(box[3] for box in bounding_boxes)

    padding_left=3
    padding_right =3
    padding_bottom =3
    padding_top =3
    x_min -= padding_left
    y_min -= padding_bottom
    x_max += padding_top
    y_max += padding_right

    # Draw the enclosing bounding rectangle
    # cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255),1)
    # print(len(contours))

    cropped_img = img[y_min:y_max, x_min:x_max]

    
    img = cv2.resize(cropped_img, (28, 28), interpolation=cv2.INTER_AREA)
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    

    img_bin = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,6)
    thres_rgb= cv2.cvtColor(img_bin,cv2.COLOR_GRAY2BGR)

    transformed_img =  img_transforms(thres_rgb).unsqueeze(dim=0)
    return transformed_img
