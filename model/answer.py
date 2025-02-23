import logging
import sys

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# 이미지 크기 설정
IMG_HEIGHT = 128
IMG_WIDTH = 128

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


def load_and_preprocess_image(image_path):
    """이미지를 로드하고 전처리합니다."""
    try:
        # 이미지 로드 및 크기 조정
        img = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
        
        # 이미지를 배열로 변환
        img_array = img_to_array(img)
        
        # 배치 차원 추가
        img_array = np.expand_dims(img_array, axis=0)
        
        # 픽셀값 정규화
        img_array = img_array / 255.0
        
        return img_array
    
    except Exception as e:
        log.error("이미지 로드 중 오류 발생: %s", str(e))
        return None


def predict_image(model, image_array):
    """이미지가 음식인지 예측합니다."""
    try:
        # 예측 수행
        prediction = model.predict(image_array, verbose=0)
        
        # 예측 결과 해석 (0.5를 임계값으로 사용)
        is_food = prediction[0][0] >= 0.5
        confidence = prediction[0][0] if is_food else 1 - prediction[0][0]
        
        return is_food, confidence
    
    except Exception as e:
        log.error("예측 중 오류 발생: %s", str(e))
        return None, None


def main():
    if len(sys.argv) != 2:
        print("사용법: python answer.py <이미지_경로>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    try:
        # 모델 로드
        log.info("모델을 로드하는 중...")
        model = load_model('food_classifier_model.h5')
        
        # 이미지 전처리
        log.info("이미지를 처리하는 중...")
        image_array = load_and_preprocess_image(image_path)
        
        if image_array is None:
            log.error("이미지 처리 실패")
            sys.exit(1)
        
        # 예측 수행
        is_food, confidence = predict_image(model, image_array)
        
        if is_food is None:
            log.error("예측 실패")
            sys.exit(1)
        
        # 결과 출력
        result = "음식" if is_food else "음식이 아님"
        print(f"\n결과: {result} (확률: {confidence:.2%})")
        
    except Exception as e:
        log.error("오류 발생: %s", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main() 