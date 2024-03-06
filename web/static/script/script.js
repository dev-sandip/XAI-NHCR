
const fileInput = document.getElementById('file-input');
const button = document.getElementById('button');
const errorMessage = document.getElementById('error-message');
const container = document.getElementById('container');

const imageContainer = document.getElementById('image-container');
const previewImage = document.getElementById('file-image');
const resultImage = document.getElementById('result-image');


const fileTitle = document.querySelector(".title");
const predInfo = document.querySelector(".pred-info");

const predictedValue = document.querySelector(".pred-info h3 span");


const topPred = document.querySelector(".pred-info ul");



const sendByCanvas = document.getElementById("canvas-send");


function createBlobFromImageData(imageData, mimeType = "image/jpeg") {
    const buffer = new ArrayBuffer(imageData.length);
    const view = new Uint8Array(buffer);
    for (let i = 0; i < imageData.length; i++) {
        view[i] = imageData.charCodeAt(i);
    }

    return new Blob([buffer], { type: mimeType });
}


function initialState() {
    button.textContent = 'Choose file';
    predInfo.style.display = 'none';
    fileTitle.textContent = "Upload your file here";
    imageContainer.style.display = 'none';
}

function displayError(message, timeout = 3000) { // Set default timeout if needed
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    initialState();
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, timeout);
}


async function sendImageToServer(image, filename) {



    // Send the file to the server using Fetch API
    try {
        const formData = new FormData();

        console.log(image)

        const base64Data = image.split(',')[1];

        formData.append('file-input-64', base64Data);




        // formData.append('file-name', filename);

        // console.log(`form data ${formData}`);


        predInfo.style.display = 'none';
        button.textContent = 'Processing....';
        fileTitle.textContent = filename;



        console.log("Submit button is clicked");

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        topPred.innerHTML = "";
        console.log('I am here')

        const jsonData = await response.json();

        console.log(jsonData)
        console.log(typeof (jsonData))
        const jsonObject = JSON.parse(jsonData);

        if (!response.ok) {
            throw new Error(`Error uploading file: ${jsonData.error}`);
        }

        resultImage.src = `data:image/jpeg;base64,` + jsonObject["ig"];
        predInfo.style.display = 'flex';

        predictedValue.textContent = `${jsonObject.item[0]} ( ${(jsonObject.prob[0] * 100).toFixed(3)}%)`;

        for (let index = 0; index < jsonObject.item.length; index++) {
            const newItem = document.createElement("li");
            newItem.textContent = `${jsonObject.item[index]} ( ${(jsonObject.prob[index] * 100).toFixed(3)}%)`
            topPred.appendChild(newItem);
        }


        // Handle successful upload response (e.g., display message)
        console.log('File uploaded successfully!');

    } catch (error) {
        // errorMessage.textContent = `Error uploading file: ${error.message}`;
        displayError(error.message);
    } finally {
        // Hide progress message (optional)
        button.textContent = 'Choose file';
    }
}

async function sentImageDataToSeverViaImage(event) {

    const file = event.target.files[0];
    const allowedExtensions = ['jpeg', 'jpg'];

    const extension = file.name.split('.').pop().toLowerCase();


    // console.log(extension);

    if (!allowedExtensions.includes(extension)) {
        event.target.value = ''; // Clear file selection
        displayError('Invalid file format. Please upload a JPG or JPEG image.')
    } else {


        const reader = new FileReader();


        reader.onload = function (event) {
            previewImage.src = event.target.result;
            resultImage.src = '';

            imageContainer.style.display = 'flex';

        };

        reader.readAsDataURL(file); // Read the file and convert it to a data URL


        // Send the file to the server using Fetch API
        try {
            const formData = new FormData();
            formData.append('file-input', file);



            button.textContent = 'Processing....';
            fileTitle.textContent = file.name;
            predInfo.style.display = 'none';




            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Error uploading file: ${response.statusText}`);
            }

            topPred.innerHTML = "";

            const jsonData = await response.json();

            console.log(jsonData)
            console.log(typeof (jsonData))
            const jsonObject = JSON.parse(jsonData);


            resultImage.src = `data:image/jpeg;base64,` + jsonObject["ig"];
            predInfo.style.display = 'flex';

            predictedValue.textContent = `${jsonObject.item[0]} ( ${(jsonObject.prob[0] * 100).toFixed(3)}%)`;

            for (let index = 0; index < jsonObject.item.length; index++) {
                const newItem = document.createElement("li");
                newItem.textContent = `${jsonObject.item[index]} ( ${(jsonObject.prob[index] * 100).toFixed(3)}%)`
                topPred.appendChild(newItem);
            }


            // Handle successful upload response (e.g., display message)
            console.log('File uploaded successfully!');

        } catch (error) {
            errorMessage.textContent = `Error uploading file: ${error.message}`;
        } finally {
            // Hide progress message (optional)
            button.textContent = 'Choose file';
        }
        errorMessage.style.display = 'none'; // Hide the error message
    }
}


async function sentImageDataToSeverViaCanvas() {
    const canvas = document.getElementById('drawing-board'); // Replace with your canvas ID
    var dataURL = canvas.toDataURL("image/jpeg");

    previewImage.src = dataURL;
    resultImage.src = '';

    imageContainer.style.display = 'flex';

    // // Create a dummy link text
    // var a = document.createElement('a');
    // // Set the link to the image so that when clicked, the image begins downloading
    // a.href = dataURL
    // // Specify the image filename
    // a.download = 'canvas-download.jpeg';
    // // Click on the link to set off download
    // a.click();

    closeDialog();

    await sendImageToServer(dataURL, 'canvas_image.jpeg');




}



button.addEventListener('click', () => {
    errorMessage.style.display = 'none';
    fileInput.click();
});




sendByCanvas.addEventListener('click', async () => {



    sentImageDataToSeverViaCanvas();
});


fileInput.addEventListener('change', async (event) => {
    sentImageDataToSeverViaImage(event);
});