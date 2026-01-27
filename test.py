from picamera2_webstream import FFmpegStream, create_ffmpeg_app

stream = FFmpegStream(
    width=1280,
    height=720,
    framerate=30,
    device='/dev/video0'
).start()

app = create_ffmpeg_app(stream)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))