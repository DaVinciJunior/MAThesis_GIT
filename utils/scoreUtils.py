from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt

def show_score(X,Y,clf,title):
    print("\t###\t" + title + "\t###\t")
    predictions = clf.predict(X)
    # print('accuracy: ' + str(accuracy_score(y_test, predictions)))
    # print('f1 score: ' + str(f1_score(y_test, predictions)))
    print(classification_report(Y, predictions))
    cm = confusion_matrix(Y, predictions, labels=clf.classes_, normalize='true')
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
    disp.plot()
    plt.title(title)
    plt.show(block=False)
    print("\t####################\t", end="\n\n")