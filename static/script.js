document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('uploadForm');
    const statusMessage = document.getElementById('statusMessage');
    const uploadedImage = document.getElementById('uploadedImage');
    const analyseButton = document.getElementById('analyseButton');
    const formContainer = document.getElementById('formContainer');
    const resubmitButton = document.getElementById('resubmitButton');
    const mainTitle = document.getElementById('mainTitle');
    const subTitle = document.getElementById('subTitle');
    const imageLoadingOverlay = document.getElementById('imageLoadingOverlay');

    resubmitButton.addEventListener('click', function () {
        form.reset();
        statusMessage.innerHTML = '';
        uploadedImage.src = '';
        form.style.display = 'block';
        formContainer.style.display = 'block';
        resubmitButton.style.display = 'none';
        mainTitle.innerHTML = 'Upload QR to Analyse';
        subTitle.innerHTML = ''
    });

    analyseButton.addEventListener('click', function () {
        imageLoadingOverlay.style.display = 'flex';
        setTimeout(() => {
            imageLoadingOverlay.style.display = 'none';
        }, 1000);
    });

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        const formData = new FormData(form);

        try {
            imageLoadingOverlay.style.display = 'flex';
            const response = await fetch('/analyse_image', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            setTimeout(() => {
                imageLoadingOverlay.style.display = 'none';    
                const pre = document.createElement('pre');
                pre.innerText = JSON.stringify(data, undefined, 2);
                pre.style.textAlign = 'left';
                pre.style.margin = '0';
                statusMessage.innerHTML = '';
                statusMessage.appendChild(pre);

                if (data.status === 'success') {
                    if (data.prediction.class === 'benign') statusMessage.style.color = '#2ecc71';
                    else statusMessage.style.color = '#e74c3c';
                    uploadedImage.src = data.file_path;
                    uploadedImage.style.display = 'block';
                    mainTitle.innerHTML = `Analysis Completed`;
                    subTitle.innerHTML = `Prediction: ${data.prediction.class}, 
                            Confidence: ${data.prediction.confidence.toFixed(2)}%, 
                            Decoded Text: <a href=${data.prediction.decoded_text}>${data.prediction.decoded_text}</a>`;
                    form.style.display = 'none';
                    formContainer.style.display = 'none';
                    resubmitButton.style.display = 'block';
                } else {
                    statusMessage.style.color = '#e74c3c';
                }
            }, 1000);
        } catch (error) {
            console.error('Error:', error);
            statusMessage.textContent = 'An error occurred while uploading the image.';
            statusMessage.style.color = '#e74c3c';  
            imageLoadingOverlay.style.display = 'none';
        }
    });

    form.addEventListener('change', function () {
        const fileInput = form.querySelector('input[type="file"]');
        analyseButton.disabled = !fileInput.files.length;
    });
});
