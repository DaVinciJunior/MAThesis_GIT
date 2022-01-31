from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

from utils import prepareTrainingDataUtils


def generate_pickle(depth=10, random_state=101):
    X, encoded_Y = prepareTrainingDataUtils.get_same_amount_of_data_for_both_classes()
    frac_test_split = 0.33
    X_train, X_test, y_train, y_test = train_test_split(X, encoded_Y, test_size=frac_test_split)

    dtree = DecisionTreeClassifier(max_depth=depth, random_state=random_state, max_features=None, min_samples_leaf=15)
    dtree.fit(X_train, y_train)
    joblib.dump(dtree, './pkl/dt.pkl')
    y_pred = dtree.predict(X_test)

    print(classification_report(y_test, y_pred))
    cm = confusion_matrix(y_test, y_pred, labels=dtree.classes_, normalize='true')
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=dtree.classes_)
    disp.plot()
    # plt.title('Confusion matrix for our classifier with kernel=linear')
    plt.show()

def load_pickle():
    return joblib.load('./pkl/dt.pkl')

def load_pickle(file_name):
    return joblib.load('./pkl/' + file_name)