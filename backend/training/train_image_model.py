import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def train_model():
    print("Starting Image Model Training...")
    
    # Data Augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    train_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )
    
    val_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )
    
    # Base model - EfficientNetB0
    base_model = tf.keras.applications.EfficientNetB0(weights='imagenet', include_top=False, input_shape=(*config.IMG_SIZE, 3))
    base_model.trainable = False
    
    # Custom Head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=config.LEARNING_RATE), 
                  loss='binary_crossentropy', 
                  metrics=['accuracy'])
    
    # Callbacks
    early_stop = tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
    checkpoint = tf.keras.callbacks.ModelCheckpoint(config.IMAGE_MODEL_PATH, save_best_only=True)
    
    print(f"Phase 1: Training custom head for {config.INITIAL_EPOCHS} epochs...")
    model.fit(
        train_generator,
        steps_per_epoch=5,
        validation_data=val_generator,
        validation_steps=2,
        epochs=config.INITIAL_EPOCHS,
        callbacks=[early_stop, reduce_lr, checkpoint]
    )
    
    # Phase 2: Fine-Tuning
    print("Phase 2: Starting fine-tuning...")
    base_model.trainable = True
    # Freeze all layers except the last 20
    for layer in base_model.layers[:-20]:
        layer.trainable = False
        
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=config.FINE_TUNE_LR),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
                  
    model.fit(
        train_generator,
        steps_per_epoch=5,
        validation_data=val_generator,
        validation_steps=2,
        epochs=config.FINE_TUNE_EPOCHS,
        callbacks=[early_stop, reduce_lr, checkpoint]
    )
    
    print(f"Improved Image model saved to {config.IMAGE_MODEL_PATH}")

if __name__ == "__main__":
    train_model()
