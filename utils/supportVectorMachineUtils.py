from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
import joblib
import matplotlib.pyplot as plt
import prepareTrainingDataUtils
import supportVectorMachineUtils

def choose_optimal_hyperparams():
    X, encoded_Y = prepareTrainingDataUtils.get_data()

    frac_test_split = 0.33
    X_train, X_test, y_train, y_test = train_test_split(X, encoded_Y, test_size=frac_test_split)

    param_grid = {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['linear', 'poly', 'rbf', 'sigmoid']}
    clf = GridSearchCV(svm.SVC(class_weight='balanced'), param_grid)
    clf = clf.fit(X_train, y_train)
    print("Best estimator found by grid search:")
    print(clf.best_estimator_)

def generate_pickle():
    # Using the same amount of data for each class did not helped boosting the performance - therefore the whole set is taken
    X, encoded_Y = prepareTrainingDataUtils.get_data()
    # Normalizing the data did not help unfortunately - it introduced more bias towards one class
    # X = prepareTrainingDataUtils.normalize_data(X)

    frac_test_split = 0.33
    X_train, X_test, y_train, y_test = train_test_split(X, encoded_Y, test_size=frac_test_split)

    # kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    # linear turned out to be the most reliant kernel -> see choose_optimal_hyperparams() method
    # clf = svm.SVC(kernel='linear', C=0.1, class_weight='balanced')
    clf = svm.SVC(kernel='linear', C=0.1, class_weight='balanced')
    clf = clf.fit(X_train, y_train)
    joblib.dump(clf, './pkl/svm.pkl')

    predictions = clf.predict(X_test)
    # print('accuracy: ' + str(accuracy_score(y_test, predictions)))
    # print('f1 score: ' + str(f1_score(y_test, predictions)))
    print(classification_report(y_test, predictions))
    cm = confusion_matrix(y_test, predictions, labels=clf.classes_, normalize='true')
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
    disp.plot()
    # plt.title('Confusion matrix for our classifier with kernel=linear')
    plt.show()

def load_pickle():
    return joblib.load('./pkl/svm.pkl')

def load_pickle(file_name):
    return joblib.load('./pkl/' + file_name)
