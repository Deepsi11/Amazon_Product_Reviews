# -*- coding: utf-8 -*-
"""Amazon_Reviews.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Kc0K8xN2HevExMHsVL2aLqYYLrby8gqk

#**DEEP LEARNING PROJECT-2**

#**TEXT CLASSIFICATION USING DEEP NEURAL NETWORKS**

#**Classify Amazon reviews using:-**

**i) convolutional neural networks and**

**ii) LSTM + attention networks. The project involves the following steps:**

**1. Collect user reviews (Amazon) that are available on internet sources**

**2. Perform pre-processing of text - removal of stop words, stemming / lemmatization, ...**

**3. Split the data into train and test tests (80% train and 20% test)**

**4. Use either GloVe or Word2Vec to represent words as numerical vectors**

**5. Train CNN , LSTM + Attention networks using your own architectures on training data**

**6. Validate the model on the test data**

**7. Fine tune the parameters to increase the classification accuracies of the model on training and test data.**

##**IMPORTING THE LIBRARIES**
"""

# IMPORTING THE DEPENDENCIES
import pandas as pd
import numpy as np
from sklearn.utils import resample,shuffle
import re

"""##**LOADING THE DATASET**"""

# LOADING THE FILE
df=pd.read_csv('/content/amazon (1) (1).csv')

# CHOOSING ONLY RELEVANT COLUMNS FROM THE DATASET
df = df[['overall','reviewText']]

"""##**DATA PRE-PROCESSING**"""

# DISPLAYING THE TOP 5 DATA POINTS FROM WHOLE DATASET
df.head()

# CHECKING FOR NULL VALUES IF ANY
df.isnull().sum()

# DROPPING THE FOUND NULL VALUES
df = df.dropna()

# RECHECKING THE NULL VALUES
df.isnull().sum()

# PUTTING CONDITIONS FOR POSITIVE AND NEGATIVE REVIEWS
# IF RATING IS >= 4 THEN ASSIGNING POSITIVE LABEL OTHERWISE NEGATIVE LABEL
conditions = [(df['overall']>=4),(df['overall']<=3)]
values =["Positive","Negative"]

# ADDING "LABEL" COLUMN TO DATAFRAME CONSITIVE POSITIVE OR POSITIVE LABELS
df['label'] = np.select(conditions,values)

# CHECKING THE TOP 5 DATAPOINTS FROM THE DATASET
df.head()

# SPLITTING THE DATASET ACCORDING TO POSITIVE AND NEGATIVE LABEL
d_major =df[df['label'] == 'Positive']
d_minor =df[df['label'] == 'Negative']

# DATA UPSAMPLING
d_minor_upsampled = resample(d_minor, replace = True, n_samples = d_major.shape[0],random_state =42)

# CONCATENATE WITH MAJORITY CLASS
df = pd.concat([d_major,d_minor_upsampled])

# HAVE A LOOK AT THE DATAFRAME
df.head()

# DEFINING A FUNCTION FOR TEXT CLEANING
def clean_text(text):
  text = re.sub("([\w\.\-\_]+@[\w\.\-\_]+)", "", text)  # REMOVING SPECIAL CHARATERS OCCURING IN EMAILS
  text = re.sub("(\d+)", "", text)                      # REMOVING DIGITS
  text = re.sub("(\n+)", "", text)                      # REMOVING NEWLINE CHARACTERS
  return text

# APPLYING THE TEXT CLEANING FUNCTION ON 'reviewText' COLUMN
df["reviewText"] = df['reviewText'].apply(clean_text)

# CREATING A SINGLE STRING REPRESENTATION OF THE ENTIRE TEXT
text = ' '.join(df['reviewText'].to_list())
text

# CHECKING THE TYPE OF TEXT
type(text)

"""##**DATA VISUALIZATION**"""

# IMPORTING THE LIBRARIES
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# REPRESNTING THE TEXT IN WORD CLOUD
wordcloud = WordCloud(background_color = "black", max_words = 800, max_font_size =30,colormap= 'viridis',scale=3,random_state=32).generate(text)
fig = plt.figure(1, figsize = (15,10))
plt.axis('off')
plt.title("review word cloud")
plt.imshow(wordcloud)
plt.show()

"""##**TEXT CLEANING/PRE-PROCESSING**"""

# IMPORTING THE NEEDED LIBRARIES
import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

"""##**REMOVING STOPWORDS**"""

# DEFINING A FUNCTION TO REMOVE STOPWORDS
def remove_stopwords(text):
  stop_words = set(stopwords.words('english'))
  word_tokens = word_tokenize(text)
# converts the words in word_tokens to lower case and then checks whether
#they are present in stop_words or not
  filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
#with no lower case conversion
  filtered_sentence = []

  for w in word_tokens:
      if w not in stop_words:
          filtered_sentence.append(w)
  return filtered_sentence

# APPLYING THE 'remove_stopwords' FUNCTION TO THE TEXT
df['reviewText'] =df['reviewText'].apply(remove_stopwords)

"""##**TOKENISING**"""

# DEFINING A TOKENIZING FUNCTION
def tokenizing(review):
  tokens = nltk.word_tokenize(review)
  return tokens

"""#**STEMMING**"""

# DEFINING A STEMMING FUNCTION
def stemming(text):

  ps = PorterStemmer()
  filsent =[]
  for w in text:
     filsent.append(ps.stem(w))
  return filsent

# APPLYING THE STEMMING FUNCTION ON REVIEWS COLUMN
df['reviewText'] =df['reviewText'].apply(stemming)

# HAVING A LOOK AT THE COLUMN
df['reviewText']

"""##**Using "Word2Vec" To Represent Words As Numerical Vectors**"""

# IMPORTING THE DEPENDENCIES
from gensim.models.word2vec import Word2Vec
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# CREATING A LIST OF REVIEWS FROM 'reviewText' COLUMN
review = []
for i in df['reviewText']:
    review.append(i)

# EXTRACTING FIRST TWO REVIEW TEXT FROM LIST
review[:2]

# USING THE WORD2VEC MODEL FROM THE GENSIM LIBRARY TO TRAIN A WORD2VEC MODEL ON A LIST OF REVIEW TEXTS.
word2vec_model = Word2Vec(review, vector_size=500, window=3, min_count=1, workers=16)

# PRINTING THE MODEL
print(word2vec_model )

# USING THE 'TOKENIZER' CLASS FROM THE 'KERAS' LIBRARY TO CONVERT TEXT DATA INTO SEQUENCE OF INEGERS.
# AND THEN USING "PAD_SEQUENCES" O ENSURE THAT THESE SEQUENCES HAVE A CONSISTENT LENGTH.
token = Tokenizer(7471)
token.fit_on_texts(df['reviewText'])
text = token.texts_to_sequences(df['reviewText'])
text = pad_sequences(text, 75)
print(text[:2])

"""##**Label Encoding**"""

# IMPORTING THE REQUIRED DEPENDENCIES
from sklearn import preprocessing
from keras.utils import to_categorical

# USING Scikit-learn's, "LabelEncoder" AND KERAS'S "to_categorical" FUNCTIONS TO PREPROCESS THE LABELS IN THE 'LABEL' COLUMN OF A DATAFRAME.
le = preprocessing.LabelEncoder()      # used to convert categorical labels into numerical labels.
y = le.fit_transform(df['label'])      # It assigns a unique numerical label to each unique category in the 'label' column
y = to_categorical(y)                  # using Keras's "to_categorical" function to convert the numerical labels into one-hot encoded vectors
y[:2]

"""##**TRAIN-TEST-SPLIT**"""

# IMPORTING THE SKLEARN'S TRAIN_TEST_SPLIT FUNCTION
from sklearn.model_selection  import train_test_split

# SPLITTING THE DATASET INTO TRAINING AND TEST SET. 80% TRAINING AND 20% TEST SET.
x_train, x_test, y_train, y_test = train_test_split(np.array(text), y, test_size=0.2, stratify=y)

#  DEFINING A FUNCTION 'gensim_to_keras_embedding' THAT CONVERTS A GENSIM WORD EMBEDDING MODEL TO KERAS EMBEDDING LAYER.
from tensorflow.keras.layers import Embedding
def gensim_to_keras_embedding(model, train_embeddings=False):
  keyed_vectors = model.wv  # structure holding the result of training
  weights = keyed_vectors.vectors  # vectors themselves, a 2D numpy array
  index_to_key = keyed_vectors.index_to_key  # which row in `weights` corresponds to which word?

  layer = Embedding(
      input_dim=weights.shape[0],
      output_dim=weights.shape[1],
      weights=[weights],
      trainable=train_embeddings,
    )
  return layer

# USING THE PREVIOUSLY DEFINED 'gensim_to_keras_embedding' FUNCTION.
wv =gensim_to_keras_embedding(word2vec_model, train_embeddings=False)

"""##**CONVOLUTIONAL NEURAL NETWORK (CNN)**"""

# IMPORTING THE LIBRARIES
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, MaxPool1D, GlobalMaxPool1D, Embedding, Activation, Input
from keras.layers import Conv2D

# DEFINING A SEQUENTIAL MODEL
keras_model = Sequential()

# ADDING THE EMBEDDING LAYER CREATED EARLIER (wv)
keras_model.add(wv)

# ADDING A DROPOUT LAYER WITH A DROPOUT RATE OF 0.2
keras_model.add(Dropout(0.2))

# ADDING TWO CONV1D LAYERS WITH 50 FILTERS, KERNEL SIZE3 3, 'RELU' ACTIVATION, 'SAME' PADDING, AND STRIDE 1.
keras_model.add(Conv1D(50, 3, activation='relu', padding='same', strides=1))
keras_model.add(Conv1D(50, 3, activation='relu', padding='same', strides=1))

# ADDING A 'MaxPool1D' LAYER
keras_model.add(MaxPool1D())

# ADDING A ANOTHER DROPOUT LAYER
keras_model.add(Dropout(0.2))

# ADDING TWO 'Conv1D' LAYERS WITH 100 FILTERS, KERNEL SIZE 3, 'RELU' ACTIVATION, 'SAME' PADDING, AND STRIDE 1
keras_model.add(Conv1D(100, 3, activation='relu', padding='same', strides=1))
keras_model.add(Conv1D(100, 3, activation='relu', padding='same', strides=1))

# Adding a MaxPool1D layer
keras_model.add(MaxPool1D())

# Adding another Dropout layer
keras_model.add(Dropout(0.2))

# Adding two Conv1D layers with 200 filters, kernel size 3, 'relu' activation, 'same' padding, and stride 1
keras_model.add(Conv1D(200, 3, activation='relu', padding='same', strides=1))
keras_model.add(Conv1D(200, 3, activation='relu', padding='same', strides=1))

# Adding GlobalMaxPool1D layer
keras_model.add(GlobalMaxPool1D())

# Adding another Dropout layer
keras_model.add(Dropout(0.2))

# A fully connected layer (Dense) with 200 units, followed by a ReLU activation.
keras_model.add(Dense(200))
keras_model.add(Activation('relu'))

# Adding another Dropout layer
keras_model.add(Dropout(0.2))

# Adding a Dense layer with 2 units (output layer for binary classification)
keras_model.add(Dense(2))
keras_model.add(Activation('softmax'))

# Compile the model with Mean Squared Error loss, accuracy metric, and the Adam optimizer
keras_model.compile(loss='mse', metrics=['acc'], optimizer='adam')

# Training the model on training data (x_train, y_train) for 3 epochs
# Using a batch size of 16 and provide validation data (x_test, y_test)
keras_model.fit(x_train, y_train, batch_size=16, epochs=3, validation_data=(x_test, y_test))

# Checking THE SHAPE OF THE DATA
print(x_train.shape, y_train.shape)

# HAVING A LOOK AT MODEL'S SUMMARY
keras_model.summary()

"""#**BUIDING A LONG-SHORT-TERM-MEMORY (LSTM) MODEL**"""

# IMPORTING LSTM FROM KERAS
from keras.layers import LSTM

# Initializing a sequential model
model = Sequential()

# A word embedding layer added to the model.
model.add(wv)

# Adding an LSTM layer to the model
model.add(LSTM(100, activation='relu', input_shape=(7471, 500)))

# A Dense layer with a single unit is added. This is the output layer of the model.
model.add(Dense(1))

# The model is compiled with the Adam optimizer and Mean Squared Error (MSE) as the loss function.
model.compile(optimizer='adam', loss='mse')

# The model is trained on the training data (x_train and y_train) for 5 epochs using the specified optimizer and loss function.
model.fit(x_train, y_train, epochs=5)

# Printing a summary of the model
model.summary()

"""#**Validating the  Model on Test Data**

---



---



"""

# Training a Keras model on the training data for 12 epochs using a batch size of 100
history = keras_model.fit(x_train, y_train, epochs=12, batch_size=100, validation_data=(x_test,y_test))

# Importing Matplotlib
import matplotlib.pyplot as plt

# Creating a plot that displays the training and validation accuracy of a neural network model over multiple epochs
plt.plot(history.history[ 'acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Creating a plot that illustrates the training and validation loss of a neural network model over multiple epochs
loss_train = history.history['loss']
loss_val = history.history['val_loss']
epochs = range(0,12)
plt.plot(epochs, loss_train, 'g', label='Training loss')
plt.plot(epochs, loss_val, 'b', label='validation loss')
plt.title('Training and Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# To evaluate the performance of a trained model on a specified test dataset.
loss, accuracy = keras_model.evaluate(x_test,y_test)

"""#**BUILING AN "ATTENTION" NETWORK**"""

#It allows you to write code that can run on multiple backends
import keras.backend as K

# The Attention layer is used for implementing attention mechanisms in neural networks.
from keras.layers import Attention

# This is used to create word embeddings
from keras.layers import Embedding

# The Bidirectional layer wraps another layer (such as an LSTM)
# And processes the input sequence in both forward and backward directions.
from keras.layers import Bidirectional

# The Adam optimizer is an optimization algorithm used for training neural networks.
from keras.optimizers import Adam

# The 'EarlyStopping' callback is used during model training to stop the
# training process if a monitored metric (such as validation loss) stops improving.
from keras.callbacks import EarlyStopping

# The Model class is used to instantiate a Keras model.
from keras import Model

# The Layer class is the base class for all layers in Keras.
from keras.layers import Layer

# The plot_model function is used to create a visual representation (plot) of a Keras model.
from keras.utils import plot_model

# 'Precision' and 'Recall' measures the proportion of correctly predicted positive instances
# among the predicted positives (precision) and among the actual positives (recall)
from keras.metrics import Precision, Recall

"""#**LSTM + ATTENTION NETWORK**"""

# This layer is defined as a subclass of Layer in Keras.
class attention(Layer):
    def __init__(self,**kwargs):
        super(attention,self).__init__(**kwargs)

    def build(self,input_shape):
        self.W=self.add_weight(name='attention_weight', shape=(input_shape[-1],1),
                               initializer='random_normal', trainable=True)
        self.b=self.add_weight(name='attention_bias', shape=(input_shape[1],1),
                               initializer='zeros', trainable=True)
        super(attention, self).build(input_shape)
    def call(self, x):
        e = K.tanh(K.dot(x, self.W) + self.b)
        e = K.squeeze(e, axis=-1)
        alpha = K.softmax(e)
        alpha = K.expand_dims(alpha, axis=-1)
        context = x * alpha
        context = K.sum(context, axis=1)
        return context

# This function defines a binary classification model using Keras.
def lstm_model(input_len, max_features=10000, embed_size=128):
    input_layer = Input(shape=(input_len,), dtype="int32")
    embedded_layer = Embedding(max_features, embed_size)(input_layer)
    lstm_layer = Bidirectional(LSTM(64, return_sequences = True))(embedded_layer)
    attention_layer = attention()(lstm_layer)
    output_layer = Dense(1, activation='sigmoid')(attention_layer)

    model = Model(input_layer, output_layer)
    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=1e-3),
                  metrics=['accuracy', Precision(), Recall()])
    return model

# LET'S SEE A QUICK SUMMARY OF THE MODEL ARCHITECTURE
model = lstm_model(input_len=75, max_features=10000, embed_size=128)
model.summary()

# MODEL WILL STOP TRAINING IF TRAINING LOSS DOESN'T IMPROVE
early_stopping = EarlyStopping(monitor='loss', patience=3, verbose=1)

"""#**FITTING AND COMPILING THE MODEL**"""

# FITTING AND COMPILING THE MODEL
history = model.fit(x_train, y_train, epochs=20, batch_size=100, verbose=1, callbacks=[early_stopping])
model.add(Dense(1, activation='sigmoid'))
y_train = y_train.reshape((-1, 1))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print("x_train shape:", x_train.shape)
print("y_train shape:", y_train.shape)
import numpy as np
x_train = np.array(x_train, dtype=np.float32)
y_train = np.array(y_train, dtype=np.float32)

# CHECKING THE KEYS
history_ = history.history
print(history_.keys())

"""#**PLOTTING THE TRAINING LOSS**"""

# PLOTTING THE TRAINING LOSS
history_ = history.history
loss = history_["loss"]
epochs = range(len(loss))

plt.plot(epochs, loss, 'b', label='Training Loss')
plt.title('Training Loss')
plt.legend()
plt.show()