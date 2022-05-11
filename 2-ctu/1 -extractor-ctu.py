#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''Seção dos imports'''
import os
import pandas as pd

'''Seção de variáveis globais'''
p_raiz1 = '/home/anderson/trabalhos/1-tese/temp/'  # Define onde os pacotes separados por segundo estão
p_resultado1 = '/home/anderson/trabalhos/'  # Define onde o CSV com os resultados devem ser salvos
replace_file = "##REPLACE##"  # Define uma chave para ser trocada pelo endereço do arquivo analisado
replace_network = "##REPLACENETWORK##"  # Define uma chave para ser trocada pelo segmento de rede analisado
comando = "tshark -r " + replace_file + " -Y \"ip.src == " + replace_network + ".0.0.0/2\" | wc -l"  # Neste comando o tshark vai contabilizar a quantidade de pacotes em um pcap separado por um segmento de rede. O pcap e o segmento de rede serão definidos pela execução do script.
list_netWork = ["1", "64", "128", "192"]  # lista com os segmentos de redes a serem analisados


def executar_comando(executar):
    ''' Este método utiliza uma função da biblioteca OS para executar um comando "no bash". Deste modo, este método realiza o cálculo de pacotes
    :param executar: comando a ser executado
    :return um inteiro com a quantidade de pacotes por segundo para o agente analisado.
    '''
    stream = os.popen(executar)
    return int(str(stream.read()).replace("\n", ""))


def contar_pacotes_por_pcap(pasta_raiz, pasta_resultado):
    ''' Este método vai contabilizar a quantidade de pacotes por pcap em uma pasta.

    :param:pasta_raiz é uma string contendo o endereço da pasta com os pcaps.
    :param:pasta_resultado é uma string indicando onde os resultados devem ser salvos.
    '''
    result = sorted(os.listdir(pasta_raiz))

    for network in list_netWork:
        time = []
        custom_lines = []
        for idx, file in enumerate(result):
            cmd = comando.replace(replace_file, pasta_raiz + file).replace(replace_network, network)
            resultado = executar_comando(cmd)
            custom_lines.append(resultado)
            time.append(idx)
            print(cmd + " === " + str(resultado))
        print(custom_lines)
        d = {"Time": time, 'x': custom_lines}
        df = pd.DataFrame(d)
        df.to_csv(pasta_resultado + network + ".csv")


if __name__ == "__main__":
    ''' Método principal do sistema, ele inicia o processamento do pcap. '''
    contar_pacotes_por_pcap(p_raiz1, p_resultado1)

