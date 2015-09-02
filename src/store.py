import pandas as pd
import time
import datetime
import sys

import os.path
import os
import logging
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('nbagg')

#from sklearn.learning_curve import learning_curve
from sklearn.externals import joblib
from sklearn import linear_model, ensemble, neighbors, svm, kernel_ridge, tree

class TrainingTracker:
    def __init__(self, path, X, y):
        self.path = path
        self.score_columns = ["model", "params", "train_score", "test_score", "train_time", "train_complete", "score_time", "model_bytes", "timestamp"]
        self.score_file = os.path.join(self.path, "scores.pkl")
        self.best_file = os.path.join(self.path, "bestmodel.pkl")
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        if os.path.isfile(self.score_file):
            self.scores = joblib.load(self.score_file)
            self.max_score = self.scores["test_score"].max()
        else:
            self.scores = pd.DataFrame(columns=self.score_columns)
            self.max_score = 0
        self.X = X
        self.y = y
        self.num_points = len(X)
        self.num_features = #TODO fix this
        self.num_classes =
        self.logger = logging.getLogger(path)

    def standard_regs(self):
        yield linear_model.LinearRegression()

        yield linear_model.LogisticRegression(penalty="l1")
        yield linear_model.LogisticRegression(penalty="l2")

        yield tree.DecisionTreeRegressor(max_depth=5)
        yield naive_bayes.GaussianNB()
        yield lda.LDA()
        yield qda.QDA()

        yield ensemble.RandomForestRegressor(n_jobs=-1, n_estimators:16)
        yield ensemble.RandomForestRegressor(n_jobs=-1, n_estimators:64)
        yield ensemble.RandomForestRegressor(n_jobs=-1, n_estimators:256)
        yield ensemble.RandomForestRegressor(n_jobs=-1, n_estimators:1024)

        yield ensemble.ExtraTreesRegressor(n_jobs=-1, n_estimators:16)
        yield ensemble.ExtraTreesRegressor(n_jobs=-1, n_estimators:64)
        yield ensemble.ExtraTreesRegressor(n_jobs=-1, n_estimators:256)
        yield ensemble.ExtraTreesRegressor(n_jobs=-1, n_estimators:1024)

        yield ensemble.AdaBoostRegressor(n_jobs=-1, n_estimators:16)
        yield ensemble.AdaBoostRegressor(n_jobs=-1, n_estimators:64)
        yield ensemble.AdaBoostRegressor(n_jobs=-1, n_estimators:256)
        yield ensemble.AdaBoostRegressor(n_jobs=-1, n_estimators:1024)

        yield svm.SVR(kernel='rbf', max_iter=2000)
        yield svm.SVR(kernel='linear', max_iter=2000)
        yield svm.SVR(kernel='sigmoid', max_iter=2000)
        yield svm.SVR(kernel='poly', max_iter=2000)
        yield kernel_ridge.KernelRidge(kernel='rbf', max_iter=2000)
        yield kernel_ridge.KernelRidge(kernel='linear', max_iter=2000)
        yield kernel_ridge.KernelRidge(kernel='sigmoid', max_iter=2000)
        yield kernel_ridge.KernelRidge(kernel='poly', max_iter=2000)

    def standard_clfs(self):
        yield linear_model.RidgeClassifier(tol=1e-2, solver="lsqr")
        yield linear_model.Perceptron(n_iter=50)
        yield linear_model.PassiveAgressiveClassifier(n_iter=50)

        yield tree.DecisionTreeClassifier(max_depth=5)
        yield naive_bayes.GaussianNB()
        yield lda.LDA()
        yield qda.QDA()

        yield ensemble.RandomForestClassifier(n_jobs=-1, n_estimators:16)
        yield ensemble.RandomForestClassifier(n_jobs=-1, n_estimators:64)
        yield ensemble.RandomForestClassifier(n_jobs=-1, n_estimators:256)
        yield ensemble.RandomForestClassifier(n_jobs=-1, n_estimators:1024)

        yield ensemble.ExtraTreesClassifier(n_jobs=-1, n_estimators:16)
        yield ensemble.ExtraTreesClassifier(n_jobs=-1, n_estimators:64)
        yield ensemble.ExtraTreesClassifier(n_jobs=-1, n_estimators:256)
        yield ensemble.ExtraTreesClassifier(n_jobs=-1, n_estimators:1024)

        yield ensemble.AdaBoostClassifier(n_jobs=-1, n_estimators:16)
        yield ensemble.AdaBoostClassifier(n_jobs=-1, n_estimators:64)
        yield ensemble.AdaBoostClassifier(n_jobs=-1, n_estimators:256)
        yield ensemble.AdaBoostClassifier(n_jobs=-1, n_estimators:1024)

        yield neighbors.KNeighborsClassifier(n_neighbors=1)
        yield neighbors.KNeighborsClassifier(n_neighbors=3)
        yield neighbors.KNeighborsClassifier(n_neighbors=5)
        yield neighbors.KNeighborsClassifier(n_neighbors=7)

        yield svm.SVC(kernel='rbf', max_iter=2000)
        yield svm.SVC(kernel='linear', max_iter=2000)
        yield svm.SVC(kernel='sigmoid', C=20, max_iter=2000)
        yield svm.SVC(kernel='poly', degree=2, max_iter=2000)

        yield Classifier(
            layers=[
                Layer("Rectifier", name="fc0", units=100),
                Layer("Rectifier", name="fc1", units=100),
                Layer("Softmax")
            ],
            learning_rate=0.01,
            learning_rule='momentum',
            learning_momentum=0.9,
            batch_size=250,
            valid_size=0.1,
            n_stable=20,
            n_iter=400,
            verbose=True)
        yield Classifier(
            layers=[
                Layer("Rectifier", name="fc0", units=100),
                Layer("Softmax")
            ],
            learning_rate=0.01,
            learning_rule='momentum',
            learning_momentum=0.9,
            batch_size=250,
            valid_size=0.1,
            n_stable=20,
            n_iter=400,
            verbose=True)
        yield Classifier(
            layers=[
                Layer("Sigmoid", name="fc0", units=100),
                Layer("Softmax")
            ],
            learning_rate=0.01,
            learning_rule='momentum',
            learning_momentum=0.9,
            batch_size=250,
            valid_size=0.1,
            n_stable=20,
            n_iter=400,
            verbose=True)

    def train_suite(self, clfs):
        for clf in clfs:
            train(clf)

    def log_run(self, clf, run):
        run["model"] = clf.__name__
        run["params"] = clf.get_params(true)
        run["model_bytes"] = sys.getsizeof(clf)
        run["timestamp"] = datetime.now().isoformat()

        test_score = run["test_score"]
        train_time = run["train_time"]
        if (test_score >= self.max_score) {
            self.logger.warning("Better model %.3f >= %.3f : %.1f s", test_score, self.max_score, train_time)
            self.max_score = test_score
            joblib.dump(clf, self.best_file)
        } else {
            self.logger.warning("Lesser model %.3f <  %.3f : %.1f s", test_score, self.max_score, train_time)
        }
        self.logger.info(clf)
        self.scores = self.scores.append(run, ignore_index=True)
        joblib.dump(self.scores, self.score_file)

    def plot_run(self, run):
        from IPython import display
        plt.figure()
        for model, grp in self.scores.groupby(['model']):
            plt.plot(grp['train_time'], grp['test_score'], 'o', label=model)
        if (run):
            plt.plot(run["train_time"], run["test_score"], '*', color="y", s=50, label="Latest")
            plt.title('Last: %.3f; Best: %.3f' % (grp['test_score'], self.max_score))
        plt.xlabel("Train time")
        plt.ylabel("Test score")
        plt.legend(loc="best")
        plt.show()

    def train (self, clf):
        run = {}
        t0 = time.time()
        clf.fit(self.X_train, self.y_train)
        t1 = time.time()
        run["train_score"] = clf.score(self.X_train, self.y_train)
        run["test_score"] = tclf.score(self.X_test, self.y_test)
        t2 = time.time()

        run["train_time"] = t1 - t0
        run["score_time"] = t2 - t1

        run["train_complete"] =
        self.log_run(clf, run)
        return run
