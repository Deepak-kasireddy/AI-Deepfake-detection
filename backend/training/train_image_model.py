import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

train_dir = "backend/dataset/Dataset/Train"

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

model.fit(train, validation_data=val, epochs=3, steps_per_epoch=100, validation_steps=20)


model.save("backend/models/image_model.h5")