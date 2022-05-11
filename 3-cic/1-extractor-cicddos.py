#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''Seção dos imports'''
import os
import datetime
import pandas as pd

'''Seção de variáveis globais'''
p_raiz1 = '/home/anderson/trabalhos/1-tese/temp/'  # Define onde os pacotes separados por segundo estão
p_resultado1 = '/home/anderson/trabalhos/'  # Define onde o CSV com os resultados devem ser salvos
replace_file = "##REPLACE##"  # Define uma chave para ser trocada pelo endereço do arquivo analisado
replace_network = "##replace_network##"  # Define uma chave para ser trocada pelo segmento de rede analisado
comando = "tshark -r " + replace_file + " -Y \"ip.src == " + replace_network + ".0.0.0/2\" | wc -l"  # Neste comando o tshark vai contabilizar a quantidade de pacotes em um pcap separado por um segmento de rede. O pcap e o segmento de rede serão definidos pela execução do script.
comando2 = "tshark -r " + replace_file + " -T fields -e frame.time_epoch -Y \"ip.src == " + replace_network + ".0.0.0/2\" "  # Neste comando o tshark vai retornar o segundo em que os pacotes foram salvos
listNetWork = ["1", "64", "128", "192"]  # lista com os segmentos de redes a serem analisados


def contar_pacotes(executar):
    ''' Este método utiliza uma função da biblioteca OS para executar um comando "no bash". Deste modo, este método realiza o cálculo de pacotes
    :param executar: comando a ser executado
    :return um inteiro com a quantidade de pacotes por segundo para o agente analisado.
    '''
    stream = os.popen(executar)
    return int(str(stream.read()).replace("\n", ""))


def pegar_tempo(executar):
    ''' Este método utiliza uma função da biblioteca OS para executar um comando "no bash". Neste caso, o objetivo é buscar o momento (segundo) em que o pacote foi enviado retornar essa informação.
    :param executar: comando a ser executado
    :return uma string com o momento (segundo) em que os pacotes foram enviados
    '''
    stream = os.popen(executar)
    string = str(stream.read())
    list = string.split("\n")
    list.pop()
    return list


def contarPacotesPorPcap():
    ''' Este método vai contabilizar a quantidade de pacotes por pcap em uma pasta.
    '''
    for network in listNetWork:
        time = []
        list_timestamp = []
        list_utc = []
        custom_lines = []
        list_local_time = []
        for i in range(100, 138):
            cmdorigem = p_raiz1.replace(replace_file, str(i))
            result = sorted(os.listdir(cmdorigem))
            for idx, file in enumerate(result):
                cmd = comando.replace(replace_file, cmdorigem + "/" + file).replace(replace_network, network)
                print(cmd)
                resultado = contar_pacotes(cmd)
                custom_lines.append(resultado)
                time.append(idx)
                cmd2 = comando2.replace(replace_file, cmdorigem + "/" + file).replace(replace_network, network)
                list = pegar_tempo(cmd2)
                list_timestamp.append(list[0] if len(list) else '-')
                list_utc.append(
                    datetime.datetime.utcfromtimestamp(float(list[0])).strftime('%Y-%m-%d %H:%M:%S.%f') if len(
                        list) else '-')
                list_local_time.append(
                    datetime.datetime.fromtimestamp(float(list[0])).strftime('%Y-%m-%d %H:%M:%S.%f') if len(list) else
                    '-')
            d = {"Time": time, 'x': custom_lines, 'timestamp': list_timestamp, 'time -3': list_local_time,
                 "time utc": list_utc}
            print(d)
            df = pd.DataFrame(d)
            df.to_csv(p_resultado1 + network + ".csv")


if __name__ == "__main__":
    ''' Método principal do sistema, ele inicia o processamento do pcap. '''
    contarPacotesPorPcap()

