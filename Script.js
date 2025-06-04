// script.js

// প্রয়োজনীয় HTML উপাদানগুলো আইডি দিয়ে চিহ্নিত করা
const scriptInput = document.getElementById('scriptInput');
const generateVideoBtn = document.getElementById('generateVideoBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const messageDisplay = document.getElementById('messageDisplay');
const videoPlayer = document.getElementById('videoPlayer');

// 'ভিডিও তৈরি করুন' বাটনে ক্লিক করলে কী হবে তার ফাংশন
generateVideoBtn.addEventListener('click', async () => {
    const script = scriptInput.value.trim(); // টেক্সট এরিয়া থেকে স্ক্রিপ্ট নেওয়া এবং অতিরিক্ত স্পেস মুছে ফেলা

    // যদি স্ক্রিপ্ট ফাঁকা থাকে, তাহলে মেসেজ দেখিয়ে থেমে যাবে
    if (!script) {
        showMessage('দয়া করে আপনার ভিডিও স্ক্রিপ্ট লিখুন।', 'error');
        return;
    }

    // UI অবস্থা রিসেট করা
    hideVideoAndMessage();
    showLoadingSpinner();
    generateVideoBtn.disabled = true; // বাটন নিষ্ক্রিয় করা যাতে বারবার ক্লিক না হয়

    try {
        // ব্যাকএন্ড API এন্ডপয়েন্টে POST রিকোয়েস্ট পাঠানো
        // এই URL টি আপনার ব্যাকএন্ড সার্ভারের URL হবে
        const response = await fetch('/generate-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ script: script }) // স্ক্রিপ্ট JSON ফরম্যাটে পাঠানো
        });

        // যদি রেসপন্স সফল না হয় (যেমন 400, 500 এরর)
        if (!response.ok) {
            const errorData = await response.json(); // এরর মেসেজ পড়া
            throw new Error(errorData.error || 'ভিডিও তৈরি করতে সমস্যা হয়েছে।');
        }

        const data = await response.json(); // সফল রেসপন্স থেকে ডেটা পড়া (ভিডিও URL)

        // যদি ভিডিও URL পাওয়া যায়, তাহলে ভিডিও প্লেয়ার দেখাও
        if (data.videoUrl) {
            videoPlayer.src = data.videoUrl; // ভিডিও URL সেট করা
            videoPlayer.style.display = 'block'; // ভিডিও প্লেয়ার দৃশ্যমান করা
            showMessage('আপনার ভিডিও তৈরি হয়েছে!', 'success'); // সফলতার বার্তা
        } else {
            // যদি API থেকে videoUrl না আসে কিন্তু এররও না হয়
            showMessage('ভিডিও URL পাওয়া যায়নি।', 'error');
        }

    } catch (error) {
        console.error('Error generating video:', error);
        showMessage(`ত্রুটি: ${error.message || 'কিছু একটা ভুল হয়েছে।'}`, 'error'); // ত্রুটির বার্তা দেখানো
    } finally {
        hideLoadingSpinner(); // লোডিং স্পিনার লুকানো
        generateVideoBtn.disabled = false; // বাটন আবার সক্রিয় করা
    }
});

// সহায়ক ফাংশন: লোডিং স্পিনার দেখানো
function showLoadingSpinner() {
    loadingSpinner.style.display = 'block';
}

// সহায়ক ফাংশন: লোডিং স্পিনার লুকানো
function hideLoadingSpinner() {
    loadingSpinner.style.display = 'none';
}

// সহায়ক ফাংশন: মেসেজ দেখানো
function showMessage(message, type = 'info') {
    messageDisplay.textContent = message;
    messageDisplay.style.display = 'block';
    // মেসেজের ধরনের উপর ভিত্তি করে রঙ পরিবর্তন (optional)
    if (type === 'error') {
        messageDisplay.style.color = '#d35400'; // কমলা/লাল
    } else if (type === 'success') {
        messageDisplay.style.color = '#27ae60'; // সবুজ
    } else {
        messageDisplay.style.color = '#333';
    }
}

// সহায়ক ফাংশন: ভিডিও এবং মেসেজ লুকানো
function hideVideoAndMessage() {
    videoPlayer.style.display = 'none';
    videoPlayer.src = ''; // ভিডিও src রিসেট করা
    messageDisplay.style.display = 'none';
    messageDisplay.textContent = '';
}
