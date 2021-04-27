import os
import sys
import PIL
import cv2

import json
import pickle
import numpy as np

from keras.models import model_from_json
from catboost import CatBoostRegressor
import xgboost as xgb

import tensorflow as tf
from tensorflow.keras.models import Model
    
try:
    catBoost_model = pickle.load(open('CatBoostRegressorModel.pkl', 'rb'))
    xgb_model = pickle.load(open('XGBRegressor.pkl', 'rb'))
    nlp_ml_model = pickle.load(open('NLP_ML_Model.pkl', 'rb'))
    image_model = pickle.load(open('ImageModel.pkl', 'rb'))
except:
    print('Не удалось загрузить модели предсказания цены авто') 
    #log

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='car_price_predict')
    channel.queue_declare(queue='result_of_car_price_predict')

    def callback(ch, method, properties, body):
        print(f'Получен вектор признаков авто {body}')
        # тут нужно понимать что здесь нам нужна картинка, а не табличные данные. Поэтому через очередь мы ожидаем как табличные данные, так и путь к файлу
        features = json.loads(body)

        catBoost_pred = catBoost_model.predict(np.array(features.table_values).reshape(1, -1))
        xgb_pred = xgb_model.predict(np.array(features.table_values).reshape(1, -1))
        nlp_ml_pred = nlp_ml_model.predict(np.array(features.table_values).reshape(1, -1))
        
        image = cv2.imread(features.file_path)
        newImage = cv2.resize(image, (320, 240))
        image_pred = image_model.predict(newImage)

        predict = (catBoost_pred[:,0] + xgb_pred + nlp_ml_pred[:,0] + image_pred[:,0]) / 4

        channel.basic_publish(exchange='', routing_key='result_of_car_price_predict', body=json.dumps(predict))
        print(f'Предсказание стоимости авто {predict} отправлено в очередь result_of_car_price_predict')

    channel.basic_consume(queue='car_price_predict', on_message_callback=callback, auto_ack=True)

    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()

except:
    print('Не удалось подключиться к очереди')
