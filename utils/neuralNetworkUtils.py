from keras.models import Sequential
from keras.layers import Dense
from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt
import joblib
import datetime
import neuralNetworkUtils
import prepareTrainingDataUtils

def create_baseline():
    model = Sequential()

    model.add(Dense(23, input_dim=23, activation='relu'))

    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def generate_pickle():
    started = datetime.datetime.now()
    print("\n\n\n>>>Starting training NN...<<<\n\n\n")

    X, encoded_Y = prepareTrainingDataUtils.get_data()

    classifier = KerasClassifier(model=neuralNetworkUtils.create_baseline, epochs=100, batch_size=50, verbose=0)
    estimators = []
    estimators.append(('standardize', StandardScaler())) # normalize data for lesser standard deviation
    estimators.append(('mlp', classifier))
    pipeline = Pipeline(estimators)
    kfold = StratifiedKFold(n_splits=10, shuffle=True)
    results = cross_val_score(pipeline, X, encoded_Y, cv=kfold)
    print('Baseline: %.2f%% (%.2f%%)' %
          (results.mean() * 100,
           results.std() * 100))
    print("\n\n\n>>>Finished training NN... It needed " + str(datetime.datetime.now() - started) + " time...<<<\n\n\n")

    pipeline.fit(X,encoded_Y)
    joblib.dump(pipeline, './pkl/nn.pkl')

    predictions = pipeline.predict(X)
    # print('f1 score: ' + str(f1_score(encoded_Y, predictions)))
    print(classification_report(encoded_Y, predictions))
    cm = confusion_matrix(encoded_Y, predictions, labels=pipeline.classes_, normalize='true')
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=pipeline.classes_)
    disp.plot()
    # plt.title('Confusion matrix for our classifier with kernel=linear')
    plt.show()

def load_pickle():
    return joblib.load('./pkl/nn.pkl')

def load_pickle(file_name):
    return joblib.load('./pkl/' + file_name)