import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

train_dir = "../dataset/images"

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train = datagen.flow_from_directory(train_dir, target_size=(224,224), batch_size=32, class_mode='binary', subset='training')
val = datagen.flow_from_directory(train_dir, target_size=(224,224), batch_size=32, class_mode='binary', subset='validation')

base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))
base.trainable = False

model = models.Sequential([
    base,
    layers.GlobalAveragePooling2D(),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train, validation_data=val, epochs=5)

model.save("../models/image_model.h5")