import pandas
from sklearn.impute import SimpleImputer
import numpy as np
from sklearn.preprocessing import MinMaxScaler

cols = ["Lag-1 AC", "Lag-2 AC", "Lag-3 AC", "Skewness", "Kurtosis", "Smax", "Coherence factor", "AIC fold",
        "AIC hopf", "AIC null"]

raiz = "/home/anderson/trabalhos/1-tese/data/ctu/"

x_train1 = pandas.read_csv(raiz + "4-test/early1.csv", usecols=cols)
x_train64 = pandas.read_csv(raiz + "4-test/early64.csv", usecols=cols)
x_train192 = pandas.read_csv(raiz + "4-test/early192.csv", usecols=cols)
x_train128 = pandas.read_csv(raiz + "4-test/early128.csv", usecols=cols)
y_train = pandas.read_csv(raiz + "4-test/early128.csv", usecols=['label'])

x_test1 = pandas.read_csv(raiz + "3-train/early1.csv", usecols=cols)
x_test64 = pandas.read_csv(raiz + "3-train/early64.csv", usecols=cols)
x_test192 = pandas.read_csv(raiz + "3-train/early192.csv", usecols=cols)
x_test128 = pandas.read_csv(raiz + "3-train/early128.csv", usecols=cols)
y_test = pandas.read_csv(raiz + "3-train/early128.csv", usecols=['label'])

x_train = pandas.concat([x_train1, x_train64, x_train192, x_train128], axis=1)
x_test = pandas.concat([x_test1, x_test64, x_test192, x_test128], axis=1)

imp = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=-1)
imp = imp.fit(x_train)
x_train = imp.transform(x_train)
imp = imp.fit(x_test)
x_test = imp.transform(x_test)

trans = MinMaxScaler()
x_train = trans.fit_transform(x_train)
x_test = trans.fit_transform(x_test)

x_train = pandas.DataFrame(x_train)
x_test = pandas.DataFrame(x_test)
c = ["col-" + str(i) for i in range(0, 40)]
x_train.columns = c
x_test.columns = c

x_train["label"] = y_train
x_test["label"] = y_test
raiz_salvar = "/home/anderson/"
x_train.to_csv(raiz_salvar + "train-final.csv")
x_test.to_csv(raiz_salvar + "test-final.csv")
