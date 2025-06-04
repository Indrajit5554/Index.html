# Index.html
<!DOCTYPE html>
<html lang="bn"> <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>টেক্সট থেকে ভিডিও তৈরি করুন</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>আপনার টেক্সট থেকে ভিডিও তৈরি করুন</h1>

        <div class="input-section">
            <label for="scriptInput">আপনার ভিডিও স্ক্রিপ্ট এখানে লিখুন:</label>
            <textarea id="scriptInput" placeholder="আপনার স্ক্রিপ্ট এখানে লিখুন..." rows="10"></textarea>
            <button id="generateVideoBtn">ভিডিও তৈরি করুন</button>
        </div>

        <div class="output-section">
            <div id="loadingSpinner" class="spinner" style="display: none;"></div>
            <p id="messageDisplay" class="message"></p>
            <video id="videoPlayer" controls autoplay style="display: none;"></video>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
