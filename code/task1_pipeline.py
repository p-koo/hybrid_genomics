import numpy as np
import h5py, os
from six.moves import cPickle
import argparse
import matplotlib.pyplot as plt
import tensorflow as tf
import tfomics
import models

#-----------------------------------------------------------------

def load_synthetic_data(file_path):

    with h5py.File(file_path, 'r') as dataset:
        x_train = np.array(dataset['X_train']).astype(np.float32).transpose([0, 2, 1])
        y_train = np.array(dataset['Y_train']).astype(np.float32)
        x_valid = np.array(dataset['X_valid']).astype(np.float32).transpose([0, 2, 1])
        y_valid = np.array(dataset['Y_valid']).astype(np.int32)
        x_test = np.array(dataset['X_test']).astype(np.float32).transpose([0, 2, 1])
        y_test = np.array(dataset['Y_test']).astype(np.int32)

    return x_train, y_train, x_valid, y_valid, x_test, y_test

#-----------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-m", type=str, default=0.05, help="model_name")
parser.add_argument("-a", type=str, default='relu', help="activation")
parser.add_argument("-f", type=int, default=64, help="filters")
parser.add_argument("-t", type=int, default=None, help="trial")
args = parser.parse_args()

model_name = args.m
activation = args.a
trial = args.t
num_filters = args.f

# set paths
results_path = '../results_task1'
if not os.path.exists(results_path):
    os.makedirs(results_path)

# load data
data_path = '../../data'
filepath = os.path.join(data_path, 'synthetic_dataset.h5')
data = load_synthetic_data(filepath)
x_train, y_train, x_valid, y_valid, x_test, y_test = data
N, L, A = x_train.shape
num_labels = y_train.shape[1]

# build model
print(model_name)
if model_name == 'CNN':
    model = models.CNN(in_shape=(L,A), num_out=num_labels, activation=activation, 
                           num_filters=num_filters, dense_units=512, heads=8, key_size=128)
elif model_name == 'CNN2':
    model = models.CNN2(in_shape=(L,A), num_out=num_labels, activation=activation, 
                           num_filters=num_filters, dense_units=512, heads=8, key_size=128)
elif model_name == 'CNN_ATT':
    model = models.CNN_ATT(in_shape=(L,A), num_out=num_labels, activation=activation, 
                           num_filters=num_filters, dense_units=512, heads=8, key_size=128)

elif model_name == 'CNN_LSTM':
    model = models.CNN_LSTM(in_shape=(L,A), num_out=num_labels, activation=activation, 
                            num_filters=num_filters, lstm_units=128, dense_units=512)

elif model_name == 'CNN_LSTM_ATT':
    model = models.CNN_LSTM_ATT(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                num_filters=num_filters, lstm_units=128, dense_units=512, heads=8, key_size=128)
elif model_name == 'CNN_LSTM_TRANS1':
    model = models.CNN_LSTM_TRANS(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                  num_filters=num_filters, num_layers=1, heads=8, key_size=128, dense_units=512)
elif model_name == 'CNN_LSTM_TRANS2':
    model = models.CNN_LSTM_TRANS(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                  num_filters=num_filters, num_layers=2, heads=8, key_size=128, dense_units=512)
elif model_name == 'CNN_LSTM_TRANS4':
    model = models.CNN_LSTM_TRANS(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                  num_filters=num_filters, num_layers=4, heads=8, key_size=128, dense_units=512)

elif model_name == 'CNN_LSTM2':
    model = models.CNN_LSTM2(in_shape=(L,A), num_out=num_labels, activation=activation, 
                            num_filters=num_filters, lstm_units=128, dense_units=512)

elif model_name == 'CNN_LSTM2_ATT':
    model = models.CNN_LSTM2_ATT(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                num_filters=num_filters, lstm_units=128, dense_units=512, heads=8, key_size=128)
elif model_name == 'CNN_LSTM2_TRANS1':
    model = models.CNN_LSTM2_TRANS(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                  num_filters=num_filters, num_layers=1, heads=8, key_size=128, dense_units=512)
elif model_name == 'CNN_LSTM2_TRANS2':
    model = models.CNN_LSTM2_TRANS(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                  num_filters=num_filters, num_layers=2, heads=8, key_size=128, dense_units=512)
elif model_name == 'CNN_LSTM2_TRANS4':
    model = models.CNN_LSTM2_TRANS(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                  num_filters=num_filters, num_layers=4, heads=8, key_size=128, dense_units=512)

elif model_name == 'CNN2_ATT':
    model = models.CNN2_ATT(in_shape=(L,A), num_out=num_labels, activation=activation, 
                           num_filters=num_filters, dense_units=512, heads=8, key_size=128)

elif model_name == 'CNN2_LSTM':
    model = models.CNN2_LSTM(in_shape=(L,A), num_out=num_labels, activation=activation, 
                            num_filters=num_filters, lstm_units=128, dense_units=512)

elif model_name == 'CNN2_LSTM_ATT':
    model = models.CNN2_LSTM_ATT(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                num_filters=num_filters, lstm_units=128, dense_units=512, heads=8, key_size=128)
elif model_name == 'CNN2_LSTM_TRANS1':
    model = models.CNN2_LSTM_TRANS(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                  num_filters=num_filters, num_layers=1, heads=8, key_size=128, dense_units=512)
elif model_name == 'CNN2_LSTM_TRANS2':
    model = models.CNN2_LSTM_TRANS(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                  num_filters=num_filters, num_layers=2, heads=8, key_size=128, dense_units=512)
elif model_name == 'CNN2_LSTM_TRANS4':
    model = models.CNN2_LSTM_TRANS(in_shape=(L,A), num_out=num_labels, activation=activation, 
                                  num_filters=num_filters, num_layers=4, heads=8, key_size=128, dense_units=512)
else:
    print("can't find model")

model_name = model_name + '_' + activation + '_' + str(trial)

# compile model model
auroc = tf.keras.metrics.AUC(curve='ROC', name='auroc')
aupr = tf.keras.metrics.AUC(curve='PR', name='aupr')
model.compile(tf.keras.optimizers.Adam(0.001), loss='binary_crossentropy', metrics=[auroc, aupr])

# early stopping callback
es_callback = tf.keras.callbacks.EarlyStopping(monitor='val_auroc', 
                                            patience=10, 
                                            verbose=1, 
                                            mode='max', 
                                            restore_best_weights=True)
# reduce learning rate callback
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_auroc', 
                                                factor=0.2,
                                                patience=4, 
                                                min_lr=1e-7,
                                                mode='max',
                                                verbose=1) 

# train model
history = model.fit(x_train, y_train, 
                    epochs=100,
                    batch_size=100, 
                    shuffle=True,
                    validation_data=(x_valid, y_valid), 
                    callbacks=[es_callback, reduce_lr])

# save training and performance results
results = model.evaluate(x_test, y_test)
logs_dir = os.path.join(results_path, model_name+'_logs.pickle')
with open(logs_dir, 'wb') as handle:
    cPickle.dump(history.history, handle)
    cPickle.dump(results, handle)

# save model params
model_dir = os.path.join(results_path, model_name+'_weights.h5')
model.save_weights(model_dir)

# Extract ppms from filters
index = [i.name for i in model.layers].index('conv_activation')
ppms = tfomics.moana.filter_activations(x_test, model, layer=index, window=20, threshold=0.5)

# generate meme file
ppms_filtered = tfomics.moana.clip_filters(ppms, threshold=0.5, pad=3)
motif_dir = os.path.join(results_path, model_name+'_filters.txt')
tfomics.moana.meme_generate(ppms_filtered, output_file=motif_dir, prefix='filter')

# Tomtom analysis
tomtom_dir = os.path.join(results_path, model_name)
jaspar_dir = 'motif_database.txt'
output = tfomics.moana.tomtom(motif_dir, jaspar_dir, tomtom_dir, evalue=False, thresh=0.1, dist='pearson', png=None, tomtom_path='tomtom')

# motif analysis
num_filters = tfomics.moana.count_meme_entries(motif_dir)
stats = tfomics.evaluate.motif_comparison_synthetic_dataset(os.path.join(tomtom_dir,'tomtom.tsv'), num_filters)
stats_dir = os.path.join(results_path, model_name+'_stats.npy')
np.save(stats_dir, stats, allow_pickle=True)

if trial == 0:
    # visualize filters
    fig = plt.figure(figsize=(25,8))
    tfomics.impress.plot_filters(ppms, fig, num_cols=8, names=stats[2], fontsize=14)
    filter_dir = os.path.join(results_path, model_name+'_filters.pdf')
    fig.savefig(filter_dir, format='pdf', dpi=200, bbox_inches='tight')



