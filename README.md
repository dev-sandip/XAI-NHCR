# Explanable Nepali Handwritten Character Recognition System

Checkout the website: [Explanable Nepali Handwritten Character Recognition System](https://bariumc-nepalicnn.hf.space/)

Welcome to the Explanable Nepali Handwritten Character Recognition System repository! This project aims to accurately recognize handwritten characters from the Nepali script while providing explanations for the model's predictions.

## Overview

This system utilizes transfer learning, employing a pre-trained ResNet101 model. We fine-tune this model's last layer to recognize Nepali characters across 58 classes. The dataset used for training is based on a modified version of the [Nepali Handwritten Characters dataset](https://www.kaggle.com/datasets/pujan9988/nepali-handwritten-characters), which has been augmented to increase its diversity.

## Dataset

The original dataset contains 11,890 images, consisting of consonants, vowels, and digits. Through augmentation techniques like rotation, blurring, and color jittering, we expanded this dataset to a total of 71,340 images. We split these images into 80% for training, 10% for validation, and 10% for testing.

## Preprocessing

Before feeding images into the model, we apply several preprocessing steps:

1. Contour detection to isolate characters.
2. Binarization and resizing to 28x28 pixels.
3. Converting images to RGB format.
4. Normalization of images with a mean of 0.5 and standard deviation of 0.5.

## Explanations

To provide insights into the model's decision-making process, we implement the integrated gradient technique. This technique overlays pixel information on the original image, indicating which pixels positively or negatively influenced the model's prediction.

## Deployment

We've deployed this system as a web application using Flask. Users can upload files or utilize the embedded playground to draw characters for prediction. Prediction results, along with overlayed images, are displayed for better understanding.

## Performance

The system achieves an accuracy of 97.52% on the test dataset. Additional metrics such as classification reports and confusion matrices are available on the system's "About" page.

## Team Members
This project was done by our team :-

- Pujan Paudel - [GitHub](https://github.com/pujan9988)
- Saugat Kandel - [GitHub](https://github.com/Saugat913)
- Prejan Devkota - [GitHub]()
- Himal Joshi - [GitHub](https://github.com/drewjustinn)
- Sanoj Dahal - [GitHub](https://github.com/sanojDD)
  
 for a minor project at Tribhuvan University, Institute of Engineering (IOE), Purwanchal Campus, Dharan, during the 6th semester.

## Limitations

- The website is not responsive and only works on larger screens for now.
- Only the integrated gradient technique has been incorporated for Explainable Artificial Intelligence (XAI). Other techniques may be explored in future iterations.

Thank you for your interest in our Explanable Nepali Handwritten Character Recognition System! If you have any questions or feedback, feel free to reach out. Happy coding!
