import h5py
from tensorflow.keras.models import load_model
# Assuming you have a trained model stored in `model` variable

from keras.models import load_model
model = load_model("models/trained_model.hdf5")
# Assuming you have a trained Keras model stored in `model` variable

# Save the model with compression
model.save('model.h5', include_optimizer=False, compression='gzip')  # or 'lzf', 'bzip2', etc.
