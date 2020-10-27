from scipy import sparse
import numpy as np
import pandas as pd
import os
import h5py

class HindroidInferencer():

    def __init__(self, info, model_dir):
        self.load_param(model_dir)
        self.A = self.apis.isin(info.api.unique()).astype(int).values.reshape(1, -1)
        np.fill_diagonal(self.A, 1)

    def load_param(self, model_dir):
        self.apis = pd.read_csv(os.path.join(model_dir, 'APIs.csv'), names=['API']).API
        self.A_tr = sparse.load_npz(os.path.join(model_dir, 'A_reduced_tr.npz'))
        self.B_tr = sparse.load_npz(os.path.join(model_dir, 'B_reduced_tr.npz'))
        self.P_tr = sparse.load_npz(os.path.join(model_dir, 'P_reduced_tr.npz'))
        self.svm_AA = GramSVMPersistor.from_h5(os.path.join(model_dir, 'AA.h5'))
        self.svm_APA = GramSVMPersistor.from_h5(os.path.join(model_dir, 'APA.h5'))
        self.svm_ABA = GramSVMPersistor.from_h5(os.path.join(model_dir, 'ABA.h5'))
        self.svm_ABPBA = GramSVMPersistor.from_h5(os.path.join(model_dir, 'ABPBA.h5'))
        self.svm_APBPA = GramSVMPersistor.from_h5(os.path.join(model_dir, 'APBPA.h5'))

    def predict_AA(self):
        gram_test = self.A * self.A_tr.T
        return self.svm_AA.decision_function(gram_test).item()

    def predict_APA(self):
        gram_test = self.A * self.P_tr * self.A_tr.T
        return self.svm_APA.decision_function(gram_test).item()

    def predict_ABA(self):
        gram_test = self.A * self.B_tr * self.A_tr.T
        return self.svm_ABA.decision_function(gram_test).item()

    def predict_ABPBA(self):
        gram_test = self.A * self.B_tr * self.P_tr * self.B_tr * self.A_tr.T
        return self.svm_ABPBA.decision_function(gram_test).item()

    def predict_APBPA(self):
        gram_test = self.A * self.P_tr * self.B_tr * self.P_tr * self.A_tr.T
        return self.svm_APBPA.decision_function(gram_test).item()


class GramSVMPersistor():
    def __init__(self, dual_coef, support, intercept):
        self.dual_coef = dual_coef
        self.support = support
        self.intercept = intercept

    @classmethod
    def from_sklearn(cls, clf):
        return cls(clf.dual_coef_, clf.support_, clf.intercept_)

    @classmethod
    def from_h5(cls, fn):
        with h5py.File(fn, 'r') as f:
            dual_coef = f['dual_coef'][:]
            support = f['support'][:]
            intercept = f['intercept'][:]
        return cls(dual_coef, support, intercept)
    
    def save_h5(self, fn):
        with h5py.File(fn, 'w') as f:
            f.create_dataset('dual_coef', data=self.dual_coef)
            f.create_dataset('support', data=self.support)
            f.create_dataset('intercept', data=self.intercept)
    
    def decision_function(self, gram_X):
        return np.asarray(
            np.dot(self.dual_coef, gram_X[:, self.support].T) + self.intercept
        )[0]

    def predict(self, gram_X):
        return self.decision_function(gram_X) > 0
