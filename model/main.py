import tensorflow as tf
from tensorflow.keras import layers, models
import os
import numpy as np
from sklearn.model_selection import train_test_split

# 이미지 크기와 배치 사이즈 설정
IMG_HEIGHT = 128
IMG_WIDTH = 128
BATCH_SIZE = 32

def load_data():
    # 데이터셋 경로 설정
    food_dir = 'datasets/food'
    not_food_dir = 'datasets/not-food'
    
    # 이미지 데이터와 레이블 준비
    images = []
    labels = []
    
    # 음식 이미지 로드 (레이블 1)
    for img_path in os.listdir(food_dir):
        img = np.load(os.path.join(food_dir, img_path))
        images.append(img)
        labels.append(1)
    
    # 비음식 이미지 로드 (레이블 0)
    for img_path in os.listdir(not_food_dir):
        img = np.load(os.path.join(not_food_dir, img_path))
        images.append(img)
        labels.append(0)
    
    # numpy 배열로 변환
    X = np.array(images)
    y = np.array(labels)
    
    # 데이터 정규화
    X = X / 255.0
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def create_model():
    model = models.Sequential([
        # 데이터 증강 레이어 추가
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        
        # 기존 레이어들
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    
    return model

def main():
    # 데이터 로드
    X_train, X_test, y_train, y_test = load_data()
    
    # 모델 생성
    model = create_model()
    
    # 모델 컴파일
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # 모델 학습
    history = model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=BATCH_SIZE,
        validation_data=(X_test, y_test)
    )
    
    # 모델 평가
    test_loss, test_accuracy = model.evaluate(X_test, y_test)
    print(f'\n테스트 정확도: {test_accuracy:.4f}')
    
    # 모델 저장
    model.save('food_classifier_model.h5')
    print('모델이 저장되었습니다: food_classifier_model.h5')

if __name__ == '__main__':
    main()
