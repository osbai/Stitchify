import os
from app import app

def test_process_route():
    client = app.test_client()
    img_path = "static/upload.png"
    assert os.path.exists(img_path), "Provide a sample image for testing."

    with open(img_path, 'rb') as f:
        data = {
            'image': (f, 'static/upload.png'),
            'colors': '5',
            'rows': '50'
        }
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert 'processed.png' in response.get_json()['output']
