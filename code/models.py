import tensorflow as tf
from tensorflow.keras import layers, Model, Input
from tfomics.layers import MultiHeadAttention



def CNN(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', heads=8, key_size=64, dense_units=512, num_out=12):

    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=24)(nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)


def CNN2(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', heads=8, key_size=64, dense_units=512, num_out=12):

    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=4)(nn)
    nn = layers.Dropout(0.1)(nn)
    nn = layers.Conv1D(filters=num_filters, kernel_size=7, use_bias=False, padding='same')(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.MaxPool1D(pool_size=6)(nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)

def CNN_LSTM(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', lstm_units=128, dense_units=512, num_out=12):
    
    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=24)(nn)
    nn = layers.Dropout(0.1)(nn)

    forward = layers.LSTM(lstm_units//2, return_sequences=True)
    backward = layers.LSTM(lstm_units//2, activation='relu', return_sequences=True, go_backwards=True)
    nn = layers.Bidirectional(forward, backward_layer=backward)(nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)



def CNN_ATT(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', heads=8, key_size=64, dense_units=512, num_out=12):

    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=24)(nn)
    nn = layers.Dropout(0.1)(nn)

    nn, w = MultiHeadAttention(num_heads=heads, d_model=key_size)(nn, nn, nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)


def CNN_LSTM_ATT(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', lstm_units=128, heads=8, key_size=64, dense_units=512, num_out=12):

    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=24)(nn)
    nn = layers.Dropout(0.1)(nn)

    forward = layers.LSTM(lstm_units//2, return_sequences=True)
    backward = layers.LSTM(lstm_units//2, activation='relu', return_sequences=True, go_backwards=True)
    nn = layers.Bidirectional(forward, backward_layer=backward)(nn)
    nn = layers.Dropout(0.1)(nn)
    
    nn, w = MultiHeadAttention(num_heads=heads, d_model=key_size)(nn, nn, nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)


def CNN_LSTM_TRANS(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', num_layers=1, heads=8, key_size=64, dense_units=512, num_out=12):
    
    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=24)(nn)
    nn = layers.Dropout(0.1)(nn)
    
    forward = layers.LSTM(key_size // 2, return_sequences=True)
    backward = layers.LSTM(key_size // 2, activation='relu', return_sequences=True, go_backwards=True)
    nn = layers.Bidirectional(forward, backward_layer=backward)(nn)
    nn = layers.Dropout(0.1)(nn)
    
    nn = layers.LayerNormalization(epsilon=1e-6)(nn)
    for i in range(num_layers):
        nn2,_ = MultiHeadAttention(d_model=key_size, num_heads=heads)(nn, nn, nn)
        nn2 = layers.Dropout(0.1)(nn2)
        nn = layers.Add()([nn, nn2])
        nn = layers.LayerNormalization(epsilon=1e-6)(nn)
        nn2 = layers.Dense(32, activation='relu')(nn)
        nn2 = layers.Dropout(0.1)(nn2)
        nn2 = layers.Dense(key_size)(nn2)
        nn2 = layers.Dropout(0.1)(nn2)
        nn = layers.Add()([nn, nn2])
        nn = layers.LayerNormalization(epsilon=1e-6)(nn)
    
    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)



def CNN_LSTM2(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', lstm_units=128, dense_units=512, num_out=12):
    
    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=4)(nn)
    nn = layers.Dropout(0.1)(nn)

    forward = layers.LSTM(lstm_units//2, return_sequences=True)
    backward = layers.LSTM(lstm_units//2, activation='relu', return_sequences=True, go_backwards=True)
    nn = layers.Bidirectional(forward, backward_layer=backward)(nn)
    nn = layers.MaxPool1D(pool_size=6)(nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)

def CNN_LSTM2_ATT(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', lstm_units=128, heads=8, key_size=64, dense_units=512, num_out=12):

    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=4)(nn)
    nn = layers.Dropout(0.1)(nn)

    forward = layers.LSTM(lstm_units//2, return_sequences=True)
    backward = layers.LSTM(lstm_units//2, activation='relu', return_sequences=True, go_backwards=True)
    nn = layers.Bidirectional(forward, backward_layer=backward)(nn)
    nn = layers.MaxPool1D(pool_size=6)(nn)
    nn = layers.Dropout(0.1)(nn)
    
    nn, w = MultiHeadAttention(num_heads=heads, d_model=key_size)(nn, nn, nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)


def CNN_LSTM2_TRANS(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', num_layers=1, heads=8, key_size=64, dense_units=512, num_out=12):
    
    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=4)(nn)
    nn = layers.Dropout(0.1)(nn)
    
    forward = layers.LSTM(key_size // 2, return_sequences=True)
    backward = layers.LSTM(key_size // 2, activation='relu', return_sequences=True, go_backwards=True)
    nn = layers.Bidirectional(forward, backward_layer=backward)(nn)
    nn = layers.MaxPool1D(pool_size=6)(nn)
    nn = layers.Dropout(0.1)(nn)
    
    nn = layers.LayerNormalization(epsilon=1e-6)(nn)
    for i in range(num_layers):
        nn2,_ = MultiHeadAttention(d_model=key_size, num_heads=heads)(nn, nn, nn)
        nn2 = layers.Dropout(0.1)(nn2)
        nn = layers.Add()([nn, nn2])
        nn = layers.LayerNormalization(epsilon=1e-6)(nn)
        nn2 = layers.Dense(32, activation='relu')(nn)
        nn2 = layers.Dropout(0.1)(nn2)
        nn2 = layers.Dense(key_size)(nn2)
        nn2 = layers.Dropout(0.1)(nn2)
        nn = layers.Add()([nn, nn2])
        nn = layers.LayerNormalization(epsilon=1e-6)(nn)
    
    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)




def CNN2_ATT(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', pool_size=5, heads=8, key_size=64, dense_units=512, num_out=12):

    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=4)(nn)
    nn = layers.Dropout(0.1)(nn)
    nn = layers.Conv1D(filters=num_filters, kernel_size=7, use_bias=False, padding='same')(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.MaxPool1D(pool_size=6)(nn)
    nn = layers.Dropout(0.1)(nn)

    nn, w = MultiHeadAttention(num_heads=heads, d_model=key_size)(nn, nn, nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)

def CNN2_LSTM(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', lstm_units=128, dense_units=512, num_out=12):
    
    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=4)(nn)
    nn = layers.Dropout(0.1)(nn)
    nn = layers.Conv1D(filters=num_filters, kernel_size=7, use_bias=False, padding='same')(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.MaxPool1D(pool_size=6)(nn)
    nn = layers.Dropout(0.1)(nn)

    forward = layers.LSTM(lstm_units//2, return_sequences=True)
    backward = layers.LSTM(lstm_units//2, activation='relu', return_sequences=True, go_backwards=True)
    nn = layers.Bidirectional(forward, backward_layer=backward)(nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)

def CNN2_LSTM_ATT(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', lstm_units=128, heads=8, key_size=64, dense_units=512, num_out=12):

    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=4)(nn)
    nn = layers.Dropout(0.1)(nn)
    nn = layers.Conv1D(filters=num_filters, kernel_size=7, use_bias=False, padding='same')(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.MaxPool1D(pool_size=6)(nn)
    nn = layers.Dropout(0.1)(nn)

    forward = layers.LSTM(lstm_units//2, return_sequences=True)
    backward = layers.LSTM(lstm_units//2, activation='relu', return_sequences=True, go_backwards=True)
    nn = layers.Bidirectional(forward, backward_layer=backward)(nn)
    nn = layers.Dropout(0.1)(nn)
    
    nn, w = MultiHeadAttention(num_heads=heads, d_model=key_size)(nn, nn, nn)
    nn = layers.Dropout(0.1)(nn)

    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)


def CNN2_LSTM_TRANS(in_shape=(200, 4), num_filters=32, batch_norm=True, activation='relu', num_layers=1, heads=8, key_size=64, dense_units=512, num_out=12):
    
    inputs = Input(shape=in_shape)
    nn = layers.Conv1D(filters=num_filters, kernel_size=19, use_bias=False, padding='same')(inputs)
    if batch_norm:
        nn = layers.BatchNormalization()(nn)
    nn = layers.Activation(activation, name='conv_activation')(nn)
    nn = layers.MaxPool1D(pool_size=4)(nn)
    nn = layers.Dropout(0.1)(nn)
    nn = layers.Conv1D(filters=num_filters, kernel_size=7, use_bias=False, padding='same')(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.MaxPool1D(pool_size=6)(nn)
    nn = layers.Dropout(0.1)(nn)

    forward = layers.LSTM(key_size // 2, return_sequences=True)
    backward = layers.LSTM(key_size // 2, activation='relu', return_sequences=True, go_backwards=True)
    nn = layers.Bidirectional(forward, backward_layer=backward)(nn)
    nn = layers.Dropout(0.1)(nn)
    
    nn = layers.LayerNormalization(epsilon=1e-6)(nn)
    for i in range(num_layers):
        nn2,_ = MultiHeadAttention(d_model=key_size, num_heads=heads)(nn, nn, nn)
        nn2 = layers.Dropout(0.1)(nn2)
        nn = layers.Add()([nn, nn2])
        nn = layers.LayerNormalization(epsilon=1e-6)(nn)
        nn2 = layers.Dense(32, activation='relu')(nn)
        nn2 = layers.Dropout(0.1)(nn2)
        nn2 = layers.Dense(key_size)(nn2)
        nn2 = layers.Dropout(0.1)(nn2)
        nn = layers.Add()([nn, nn2])
        nn = layers.LayerNormalization(epsilon=1e-6)(nn)
    
    nn = layers.Flatten()(nn)

    nn = layers.Dense(dense_units, use_bias=False)(nn)
    nn = layers.BatchNormalization()(nn)
    nn = layers.Activation('relu')(nn)
    nn = layers.Dropout(0.5)(nn)

    outputs = layers.Dense(num_out, activation='sigmoid')(nn)

    return Model(inputs=inputs, outputs=outputs)

    

