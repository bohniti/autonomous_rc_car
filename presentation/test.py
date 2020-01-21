x = img_in
x = Convolution2D(24, (5, 5), strides=(2, 2), activation='relu')(x
x = Convolution2D(32, (5, 5), strides=(2, 2), activation='relu')(x) 
x = Convolution2D(64, (5, 5), strides=(2, 2), activation='relu')(x) 
x = Convolution2D(64, (3, 3), strides=(2, 2), activation='relu')(x) 
x = Convolution2D(64, (3, 3), strides=(1, 1), activation='relu')(x) 
x = Flatten(name='flattened')(x)  # Flatten to 1D (Fully connected)
x = Dense(100, activation='relu')(x0
x = Dense(50, activation='relu')(x)
angle_out = Dense(units=1, activation='linear', name='angle_out')
