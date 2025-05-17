from flask import Flask, request, render_template, send_from_directory
import cv2
import numpy as np
import os
app = Flask(__name__)


UPLOAD_FOLDER = "static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    image = request.files['image']
    num_colors = int(request.form['colors'])
    num_rows = int(request.form['rows'])

    # Save original upload
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'upload.png')
    image.save(img_path)

    # Load with OpenCV
    img = cv2.imread(img_path)

    # Resize to the requested number of rows (keep aspect ratio)
    h, w, _ = img.shape
    new_height = num_rows
    new_width = int(w * (new_height / h))
    img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Reduce number of colors using k-means clustering
    Z = img_resized.reshape((-1, 3)).astype(np.float32)
    _, labels, centers = cv2.kmeans(Z, num_colors, None,
                                    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
                                    10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    quantized = centers[labels.flatten()].reshape(img_resized.shape)

    # Resize back to original for display (optional)
    final = cv2.resize(quantized, (w, h), interpolation=cv2.INTER_NEAREST)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed.png')
    cv2.imwrite(output_path, final)

    return {'output': 'processed.png'}

# @app.route('/static/<path:filename>')
# def static_files(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
