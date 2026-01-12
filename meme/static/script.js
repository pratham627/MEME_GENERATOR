document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('meme-form');
    const imageInput = document.getElementById('image-input');
    const memeImage = document.getElementById('meme-image');
    const placeholderText = document.querySelector('.placeholder-text');
    const downloadBtn = document.getElementById('download-btn');
    const previewSection = document.querySelector('.preview-section');

    // Show preview of uploaded image immediately (optional, better UX)
    imageInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = (e) => {
                memeImage.src = e.target.result;
                memeImage.style.display = 'block';
                placeholderText.style.display = 'none';
                previewSection.style.border = 'none';
            }
            reader.readAsDataURL(e.target.files[0]);
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const submitBtn = form.querySelector('button');
        const originalBtnText = submitBtn.textContent;

        // simple loading state
        submitBtn.textContent = 'Generating...';
        submitBtn.disabled = true;
        memeImage.style.opacity = '0.5';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);

            // Update image
            memeImage.src = imageUrl;
            memeImage.style.display = 'block';
            memeImage.style.opacity = '1';
            placeholderText.style.display = 'none';
            previewSection.style.border = 'none';

            // Setup download link
            downloadBtn.href = imageUrl;
            downloadBtn.download = 'meme.jpg'; // default name
            downloadBtn.style.display = 'inline-block';
            downloadBtn.textContent = 'Download Meme';

        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate meme. Please try again.');
            memeImage.style.opacity = '1';
        } finally {
            submitBtn.textContent = originalBtnText;
            submitBtn.disabled = false;
        }
    });
});
