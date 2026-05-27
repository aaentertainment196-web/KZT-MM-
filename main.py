from flask import Flask, request, send_file, jsonify
import edge_tts
import asyncio
import io

app = Flask(__name__)

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text', '')
    voice = data.get('voice', 'my-MM-NilarNeural')
    if not text.strip():
        return jsonify({'error': 'No text'}), 400
    async def generate():
        communicate = edge_tts.Communicate(text, voice)
        audio_data = b''
        async for chunk in communicate.stream():
            if chunk['type'] == 'audio':
                audio_data += chunk['data']
        return audio_data
    try:
        audio_data = asyncio.run(generate())
        return send_file(
            io.BytesIO(audio_data),
            mimetype='audio/mpeg',
            download_name='audio.mp3'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
