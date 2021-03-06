#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX Audio Embedding Generator'
    assert json.get('info') and json.get('info').get('description') == 'Generate embedding vectors from audio files.'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'audio_embeddings-tf'
    assert metadata['name'] == 'audio_embeddings TensorFlow Model'
    assert metadata['description'] == 'audio_embeddings TensorFlow model trained on Audio Set'
    assert metadata['license'] == 'Apache 2.0'
    assert metadata['source'] == 'https://developer.ibm.com/exchanges/models/all/max-audio-embedding-generator/'


def test_predict():

    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'samples/car-horn.wav'

    with open(file_path, 'rb') as file:
        file_form = {'audio': (file_path, file, 'audio/wav')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200

    response = r.json()

    assert response['status'] == 'ok'

    assert len(response['embedding']) == 4
    assert len(response['embedding'][0]) == 128
    assert len(response['embedding'][1]) == 128
    assert len(response['embedding'][2]) == 128
    assert len(response['embedding'][3]) == 128


def test_invalid_mimetype():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'tests/test.py'

    with open(file_path, 'rb') as file:
        file_form = {'audio': (file_path, file, 'text/x-python')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 400

    response = r.json()

    assert response['status'] == 'error'
    assert response['message'] == 'Invalid file type/extension'


if __name__ == '__main__':
    pytest.main([__file__])
