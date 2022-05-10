#!/usr/bin/python
# -*- encoding: iso-8859-1 -*-
'''Seção dos imports'''
import pandas
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier


def ler_dados(raiz):
    '''ler os dados de treinamento e de teste do CSV
    :param local onde os arquivos estão
    :return retorna 4 DataFrames com os dados de treinamento e teste e os rótulos separados
    '''
    cols = ['col-3', 'col-4', 'col-5', 'col-7', 'col-8', 'col-9',
            'col-13', 'col-14', 'col-15', 'col-17', 'col-18', 'col-19',
            'col-23', 'col-24', 'col-25', 'col-27', 'col-28', 'col-29',
            'col-33', 'col-34', 'col-35', 'col-37', 'col-38', 'col-39']

    x_train = pandas.read_csv(raiz + "train-final.csv", usecols=cols)
    y_train = pandas.read_csv(raiz + "train-final.csv", usecols=["label"])
    x_test = pandas.read_csv(raiz + "test-final.csv", usecols=cols)
    y_test = pandas.read_csv(raiz + "test-final.csv", usecols=["label"])

    return x_train, y_train, x_test, y_test


def classify(x_train, y_train, x_test, y_test):
    '''
    Este método treina a mlp com 5 estimadores utilizando os dados de treinamento e testa o adaboost utilizando os dados de teste.
    :param x_train:
    :param y_train:
    :param x_test:
    :param y_test:
    '''
    classifier = MLPClassifier(
        solver='lbfgs',
        hidden_layer_sizes=(33, 17, 11), random_state=0,
    )
    classifier.fit(x_train, y_train)
    y_pred_test = classifier.predict(x_test)
    print("Resultados no teste")
    print(confusion_matrix(y_test, y_pred_test))
    print(classification_report(y_test, y_pred_test))
    print(*y_pred_test, sep=',')


if __name__ == "__main__":
    raiz = "/home/anderson/trabalhos/1-tese/data/cicddos2019/5-train-test-final/"
    x_train, y_train, x_test, y_test = ler_dados(raiz)
    classify(x_train, y_train, x_test, y_test)  # ctu

