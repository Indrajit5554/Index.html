# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS # যদি ফ্রন্টএন্ড এবং ব্যাকএন্ড আলাদা পোর্টে চলে
import requests
import os
from dotenv import load_dotenv

# .env ফাইল থেকে এনভায়রনমেন্ট ভেরিয়েবল লোড করা
load_dotenv()

app = Flask(__name__)
# CORS এনাবল করা, যাতে ফ্রন্টএন্ড (যেমন localhost:5000) ব্যাকএন্ড (যেমন localhost:5000) এর সাথে যোগাযোগ করতে পারে।
# আপনি চাইলে নির্দিষ্ট ডোমেইন সেট করতে পারেন: CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
CORS(app) 

# আপনার থার্ড-পার্টি API Key এবং এন্ডপয়েন্ট এনভায়রনমেন্ট ভেরিয়েবল থেকে নিন
# এটি খুবই গুরুত্বপূর্ণ যে আপনি আপনার API Key সরাসরি কোডে লিখবেন না!
THIRD_PARTY_API_KEY = os.getenv('THIRD_PARTY_API_KEY')
THIRD_PARTY_API_ENDPOINT = os.getenv('THIRD_PARTY_API_ENDPOINT') # যেমন: 'https://api.example.com/generate-video'

# নিশ্চিত করুন যে API Key এবং এন্ডপয়েন্ট সেট করা হয়েছে
if not THIRD_PARTY_API_KEY or not THIRD_PARTY_API_ENDPOINT:
    print("Environment variables THIRD_PARTY_API_KEY or THIRD_PARTY_API_ENDPOINT are not set.")
    print("Please create a .env file with these variables.")
    # এটি প্রোডাকশন এনভায়রনমেন্টে বন্ধ করা উচিত বা আরও সুন্দরভাবে হ্যান্ডেল করা উচিত
    exit(1) # যদি ভেরিয়েবল না থাকে তাহলে সার্ভার বন্ধ করে দাও

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json() # ফ্রন্টএন্ড থেকে পাঠানো JSON ডেটা গ্রহণ করা
        script = data.get('script') # স্ক্রিপ্ট বের করা

        if not script:
            return jsonify({'error': 'স্ক্রিপ্ট প্রদান করা হয়নি।'}), 400

        # থার্ড-পার্টি API-তে ডেটা পাঠানোর জন্য হেডার
        headers = {
            'Authorization': f'Bearer {THIRD_PARTY_API_KEY}', # API অথেন্টিকেশনের জন্য
            'Content-Type': 'application/json'
            # আপনার API এর প্রয়োজন অনুযায়ী অন্যান্য হেডার যোগ করুন
        }

        # থার্ড-পার্টি API-তে পাঠানোর জন্য পেলোড (ডেটা)
        # এটি আপনার নির্বাচিত API এর ডকুমেন্টেশন অনুযায়ী পরিবর্তন করতে হবে!
        payload = {
            'text': script,
            'language': 'bn', # যদি আপনার API বাংলা সমর্থন করে
            'voice_id': 'bn-female-01', # উদাহরণ: আপনার API এর ভয়েস আইডি
            # অন্যান্য প্রয়োজনীয় প্যারামিটার যোগ করুন (যেমন: background_music, video_style, etc.)
        }

        print(f"Sending request to third-party API: {THIRD_PARTY_API_ENDPOINT}")
        # থার্ড-পার্টি API-তে POST রিকোয়েস্ট পাঠানো
        response = requests.post(THIRD_PARTY_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status() # HTTP এরর হলে এক্সেপশন তৈরি করা

        # থার্ড-পার্টি API থেকে পাওয়া রেসপন্স JSON ফরম্যাটে লোড করা
        api_response_data = response.json()
        print(f"Received response from third-party API: {api_response_data}")

        # এখানে আপনাকে api_response_data থেকে ভিডিও URL বের করতে হবে।
        # এটি প্রতিটি API এর জন্য আলাদা হতে পারে। যেমন:
        # video_url = api_response_data.get('video_url')
        # video_url = api_response_data.get('data', {}).get('url')
        
        # উদাহরণের জন্য: ধরে নিলাম API রেসপন্সে সরাসরি 'videoUrl' নামে একটি কী আছে
        video_url = api_response_data.get('videoUrl') 
        
        if not video_url:
            return jsonify({'error': 'থার্ড-পার্টি API থেকে ভিডিও URL পাওয়া যায়নি।', 'api_response': api_response_data}), 500

        # ফ্রন্টএন্ডে ভিডিও URL ফেরত পাঠানো
        return jsonify({'videoUrl': video_url})

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to third-party API: {e}")
        return jsonify({'error': f'থার্ড-পার্টি API-এর সাথে সংযোগে সমস্যা: {e}'}), 502
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': f'একটি অপ্রত্যাশিত ত্রুটি হয়েছে: {e}'}), 500

if __name__ == '__main__':
    # সার্ভার চালানো
    # debug=True ডেভেলপমেন্টের সময় সুবিধাজনক, কিন্তু প্রোডাকশনে False রাখতে হবে
    app.run(debug=True, port=5000) # ডিফল্ট পোর্ট 5000
