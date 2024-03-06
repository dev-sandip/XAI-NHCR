import numpy as np 
from io import BytesIO
import cv2
from captum.attr import IntegratedGradients
from captum.attr import visualization as viz
import io
import torch 
import torchvision 
import torch.nn as nn
from torchvision import transforms,models
from torchvision.transforms import v2
import torch.nn.functional as F
torchvision.disable_beta_transforms_warning()
import json
import base64
    

index_to_target = {
0: 'अ', 1: 'अं', 2: 'अः', 3: 'आ', 4: 'इ', 5: 'ई', 6: 'उ', 7: 'ऊ', 8: 'ए', 9: 'ऐ', 10: 'ओ', 11: 'औ', 12: 'क', 13: 'क्ष', 14: 'ख', 15: 'ग', 16: 'घ', 17: 'ङ', 18: 'च', 19: 'छ', 20: 'ज', 21: 'ज्ञ', 22: 'झ', 23: 'ञ', 24: 'ट', 25: 'ठ', 26: 'ड', 27: 'ढ', 28: 'ण', 29: 'त', 30: 'त्र', 31: 'थ', 32: 'द', 33: 'ध', 34: 'न', 35: 'प', 36: 'फ', 37: 'ब', 38: 'भ', 39: 'म', 40: 'य', 41: 'र', 42: 'ल', 43: 'व', 44: 'श', 45: 'ष', 46: 'स', 47: 'ह', 48: '०', 49: '१', 50: '२', 51: '३', 52: '४', 53: '५', 54: '६', 55: '७', 56: '८', 57: '९'}
target_to_index = {value:key for key,value in index_to_target.items()}


device = 'cuda:0' if torch.cuda.is_available() else "cpu"

img_transforms = v2.Compose([
    transforms.ToTensor(),
    v2.ToDtype(torch.float32),
    v2.Normalize((0.5,),(0.5,))
])

#
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

        #neglecting very small contours which are actually noise 
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


    cropped_img = img[y_min:y_max, x_min:x_max]
    return cropped_img




def predict(image_buffer:BytesIO)->str:
    device = 'cuda:0' if torch.cuda.is_available() else "cpu"

    model_path ="res97_state.pth"
    
    model = models.resnet101(weights=None).to(device)
    num_classes = 58
    model.fc = nn.Linear(model.fc.in_features, num_classes).to(device)
    model.load_state_dict(torch.load(model_path,map_location=device))

    image_buffer.seek(0)
    
    img= cv2.imdecode(np.frombuffer(image_buffer.read(),np.uint8),-1)
    
    if img is None:
        raise RuntimeError("Failed to decode image")
    
    img = crop_characters(img)
    
    img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    

    img_bin = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,6)
    thres_rgb= cv2.cvtColor(img_bin,cv2.COLOR_GRAY2BGR)
    
    model.eval()
    
    transformed_img =  img_transforms(thres_rgb).unsqueeze(dim=0)
  
    
    
    with torch.inference_mode():
        transformed_img = transformed_img.to(device)
        outputs = model(transformed_img)
        _,predicted_index = torch.max(outputs.data,1) #returns max value and index
        probabilities = F.softmax(outputs,1)

    

    def attribute_image_features(algorithm,image , **kwargs):
        model.zero_grad()
        tensor_attributions = algorithm.attribute(image,
                                                target=predicted_index,
                                                **kwargs
                                                )
        
        return tensor_attributions

    ig = IntegratedGradients(model)
    attr_ig, delta = attribute_image_features(ig, transformed_img, baselines=transformed_img * 0, return_convergence_delta=True)
    attr_ig = np.transpose(attr_ig.squeeze().cpu().detach().numpy(), (1, 2, 0))
    

    original_image = img

    # org_img,axes1 = viz.visualize_image_attr(None, original_image, 
    #                     method="original_image", title="Original Image",use_pyplot=False)
        
    img_attr,axes2= viz.visualize_image_attr(attr_ig, original_image, method="blended_heat_map",sign="all",
                                        title="Overlayed Integrated Gradients",use_pyplot=False,show_colorbar=True)
    
    img_attr_bytes = io.BytesIO()
    img_attr.savefig(img_attr_bytes,format="jpeg")
    

    
    top3,top3index= torch.topk(probabilities,3)
    # print(top3,top3index)
    top3Value= top3.tolist()
    top3Index= top3index.tolist()
    # print(top3Value,top3Index)
    
    
    json_data_dict={
        "prob":top3Value[0],
        "item":[ index_to_target[int(item)] for item in top3Index[0]],
        "ig":base64.b64encode(img_attr_bytes.getvalue()).decode('utf-8')
       
    }
    
    return  json.dumps( json_data_dict)
    