import matplotlib.pyplot as plt
import numpy as np
from PUM1 import *
from PUM3 import *
from sklearn import datasets
# from IPython.display import Image
# %matplotlib inline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from distutils.version import LooseVersion as Version
from sklearn import __version__ as sklearn_version

class Worker:
    def do(self):
        iris = datasets.load_iris()
        X = iris.data[:, [2, 3]]
        y = iris.target
        print('Etykiety klas:', np.unique(y))

        
        if Version(sklearn_version) < '0.18':
            from sklearn.grid_search import train_test_split
        else:
            from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=0)

        sc = StandardScaler()
        sc.fit(X_train)
        X_train_std = sc.transform(X_train)
        X_test_std = sc.transform(X_test)

        

        ppn = Perceptron(n_iter_no_change=40, eta0=0.1, random_state=0)
        ppn.fit(X_train_std, y_train)
        y_test.shape

        y_pred = ppn.predict(X_test_std)
        print('Nieprawidłowo sklasyfikowane próbki: %d' % (y_test != y_pred).sum())
        print('Dokładność: %.2f' % accuracy_score(y_test, y_pred))

        X_combined_std = np.vstack((X_train_std, X_test_std))
        y_combined = np.hstack((y_train, y_test))

        # plot_decision_regions(X=X_combined_std, y=y_combined,
        #                     classifier=ppn, test_idx=range(105, 150))
        # plt.xlabel('Długość płatka [standaryzowana]')
        # plt.ylabel('Szerokość płatka [standaryzowana]')
        # plt.legend(loc='upper left')

        # plt.tight_layout()
        #plt.savefig('./rysunki/03_01.png', dpi=300)
        #plt.show()

        from sklearn.linear_model import LogisticRegression

        lr = LogisticRegression(C=100.0, random_state=0)
        lr.fit(X_train_std, y_train)

        # plot_decision_regions(X_combined_std, y_combined,
        #                     classifier=lr, test_idx=range(105, 150))
        # plt.xlabel('Długość płatka [standaryzowana]')
        # plt.ylabel('Szerokość płatka [standaryzowana]')
        # plt.legend(loc='upper left')
        # plt.tight_layout()
        # #plt.savefig('./rysunki/03_05.png', dpi=300)
        # plt.show()

        from sklearn.svm import SVC

        svm = SVC(kernel='linear', C=1.0, random_state=0)
        svm.fit(X_train_std, y_train)

        plot_decision_regions(X_combined_std, y_combined,
                            classifier=svm, test_idx=range(105, 150))
        plt.xlabel('Długość płatka [standaryzowana]')
        plt.ylabel('Szerokość płatka [standaryzowana]')
        plt.legend(loc='upper left')
        plt.tight_layout()
        #plt.savefig('./rysunki/03_10.png', dpi=300)
        plt.show()
        pass