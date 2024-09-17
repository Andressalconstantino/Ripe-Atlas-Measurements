import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
from probesLocation import probesLocation
import os

#Obtem o país de uma probe com base no seu id
def getProbeCountry(probeId):
    return probesLocation.get(probeId, {}).get('país', f'ID {probeId} não encontrado')

#Obtem o continente de uma probe com base em seu id
def getProbeContinent(probeId):
    return probesLocation.get(probeId, {}).get('continente', f'ID {probeId} não encontrado')

#Obtem a latência de cada hop de uma probe
def getLatency(probeInfo):
    latencias = []
    for hop in probeInfo['result']:
        latenciasHop = [item['rtt'] for item in hop['result'] if 'rtt' in item]
        latencias.append(latenciasHop)
    return latencias

#Processa os dados de uma probe e retorna um dicionário com os dados relevantes
def processProbeInfo(probeInfo):
    return {
        'probeId': probeInfo['prb_id'],
        'destino': probeInfo['dst_name'],
        'pais': getProbeCountry(probeInfo['prb_id']),
        'continente': getProbeContinent(probeInfo['prb_id']),
        'latencia': getLatency(probeInfo),
        'quantidadeSaltos': len(probeInfo['result']),
        'data': datetime.fromtimestamp(probeInfo['stored_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    }

#Carrega os dados de uma probe a partir de um arquivo json
def loadProbeData(file_path):
    with open(file_path, 'r') as jsonFile:
        return json.load(jsonFile)['info']

#Agrupa as probes por país
def groupProbesByCountry(probeData):
    probeGroupedInfo = {}
    for probeInfo in probeData:
        if probeInfo["destination_ip_responded"]:
            probeJson = processProbeInfo(probeInfo)
            if probeJson['probeId'] in probeGroupedInfo:
                probeGroupedInfo[probeJson['probeId']].append(probeJson['pais'])
            else:
                probeGroupedInfo[probeJson['probeId']] = [probeJson['pais']]
    return probeGroupedInfo

#Cria um gráfico de linha mostrando a variação da latência ao longo do tempo para uma probe específica
def plotLatencyOverTime(dataframe, output_dir, id):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=dataframe, x='timestamp', y='rtt', hue='destination', marker='o', errorbar=None)
    plt.title(f'Variação da Latência ao Longo do Tempo por probe (ID: {id})')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.legend(title='Destino', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'latencia_por_tempo_{id}.png'))
    #plt.show()
    plt.close()

#Cria um gráfico de linha para mostrar a variação de quantidade de saltos ao  longo do tempo para uma probe específica
def plotHopsOverTime(dataframe, output_dir, id):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=dataframe, x='timestamp', y='hop', hue='destination', marker='o', errorbar=None)
    plt.title(f'Variação da Quantidade de Saltos ao Longo do Tempo por probe (ID: {id})')
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade de Saltos')
    plt.legend(title='Destino', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'saltos_por_tempo_{id}.png'))
    # plt.show()
    plt.close()


#Cria um gráfico de dispersão mostrando a relação entre a latência e a quantidade de saltos de uma probe específica
def plotLatencyVsHops(dataframe, output_dir, id):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=dataframe, x='hop', y='rtt', hue='destination', marker='o')
    plt.title(f'Relação entre Latência e Quantidade de Saltos (ID: {id})')
    plt.xlabel('Quantidade de Saltos')
    plt.ylabel('Latência (ms)')
    plt.legend(title='Destino', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'latencia_X_saltos{id}.png'))
    # plt.show()
    plt.close()

#Cria um gráfico de linha para mostrar a latência ao longo do tempo por continente
def plotLatencyOverTimeByContinent(dataframe, output_dir):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=dataframe, x='timestamp', y='rtt', hue='continent', marker='o')
    plt.title('Média da Latência ao Longo do Tempo por Continente')
    plt.xlabel('Tempo')
    plt.ylabel('Latência Média (ms)')
    plt.legend(title='Continente', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latencia_por_tempo_por_continente.png'))
    # plt.show()
    plt.close()


#Cria um gráfico de linha para mostrar a média da quantidade de saltos ao longo do tempo por continente
def plotHopsOverTimeByContinent(dataframe, output_dir):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=dataframe, x='timestamp', y='hop', hue='continent', marker='o')
    plt.title('Média da Quantidade de Saltos ao Longo do Tempo por Continente')
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade Média de Saltos')
    plt.legend(title='Continente', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'saltos_por_tempo_por_continente.png'))
    # plt.show()
    plt.close()


# Cria um gráfico de dispersão para mostrar a relação entre latência e quantidade de saltos por continente
def plotLatencyVsHopsByContinent(dataframe, output_dir):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=dataframe, x='hop', y='rtt', hue='continent')
    plt.title('Relação entre Latência e Quantidade de Saltos por Continente')
    plt.xlabel('Quantidade de Saltos')
    plt.ylabel('Latência (ms)')
    plt.legend(title='Continente', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latencia_X_saltos_por_continente.png'))
    # plt.show()
    plt.close()


# Cria um gráfico de linha para mostrar a média da latência ao longo do tempo por país
def plotLatencyOverTimeByCountry(dataframe, output_dir):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=dataframe, x='timestamp', y='rtt', hue='country', marker='o')
    plt.title('Média da Latência ao Longo do Tempo por País')
    plt.xlabel('Tempo')
    plt.ylabel('Latência Média (ms)')
    plt.legend(title='País', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latencia_por_tempo_por_pais.png'))
    # plt.show()
    plt.close()

#Cria um gráfico de linha para mostrar a média da latência ao longo do tempo por destino
def plotLatencyOverTimeByDestination(dataframe, output_dir):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=dataframe, x='timestamp', y='rtt', hue='destination', marker='o')
    plt.title('Média da Latência ao Longo do Tempo por Destino')
    plt.xlabel('Tempo')
    plt.ylabel('Latência Média (ms)')
    plt.legend(title='Destino', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latencia_por_tempo_por_destino.png'))
    # plt.show()
    plt.close()


#Cria um gráfico de linha para mostrar a média da quantidade de saltos ao longo do tempo por destino
def plotHopsOverTimeByDestination(dataframe, output_dir):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=dataframe, x='timestamp', y='hop', hue='destination', marker='o')
    plt.title('Média da Quantidade de Saltos ao Longo do Tempo por Destino')
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade Média de Saltos')
    plt.legend(title='Destino', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'saltos_por_tempo_por_destino.png'))
    # plt.show()
    plt.close()


#Cria um gráfico de linha para mostrar a média da quantidade de saltos ao longo do tempo por país
def plotHopsOverTimeByCountry(dataframe, output_dir):
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=dataframe, x='timestamp', y='hop', hue='country', marker='o')
    plt.title('Média da Quantidade de Saltos ao Longo do Tempo por País')
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade Média de Saltos')
    plt.legend(title='País', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'saltos_por_tempo_por_pais.png'))
    # plt.show()
    plt.close()


#Cria um gráfico de dispersão para mostrar a relação entre latência e quantidade de saltos por país
def plotLatencyVsHopsByCountry(dataframe, output_dir):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=dataframe, x='hop', y='rtt', hue='country')
    plt.title('Relação entre Latência e Quantidade de Saltos por País')
    plt.xlabel('Quantidade de Saltos')
    plt.ylabel('Latência (ms)')
    plt.legend(title='País', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latencia_X_saltos_por_pais.png'))
    # plt.show()
    plt.close()

#Cria um gráfico de dispersão para mostrar a relação entre latência e quantidade de saltos por destino
def plotLatencyVsHopsByDestination(dataframe, output_dir):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=dataframe, x='hop', y='rtt', hue='destination')
    plt.title('Relação entre Latência e Quantidade de Saltos por Destino')
    plt.xlabel('Quantidade de Saltos')
    plt.ylabel('Latência (ms)')
    plt.legend(title='Destino', loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latencia_X_saltos_por_destino.png'))
    # plt.show()
    plt.close()

def main():
    #Lista de caminhos dos arquivos JSON contendo os dados das probes
    file_paths = ['jsonFiles/GoogleNews.json', 'jsonFiles/FolhaSP.json', 'jsonFiles/Reuters.json']
    combined_rows = []

    #Itera sobre cada arquivo JSON
    for file_path in file_paths:
        #Carrega os dados das probes a partir do arquivo JSON
        probeData = loadProbeData(file_path)
        #Agrupa as probes por país
        probeGroupedInfo = groupProbesByCountry(probeData)

        #Obtém a lista de países únicos
        paises = list(set([info[0] for info in probeGroupedInfo.values()]))
        
        #Itera sobre cada país
        for pais in paises:
            probeGroupedInfo = {}
            #Itera sobre cada probe
            for probeInfo in probeData:
                #Verifica se a probe respondeu ao destino e se pertence ao país atual
                if probeInfo["destination_ip_responded"] and getProbeCountry(probeInfo['prb_id']) == pais:
                    #Processa as informações da probe
                    probeJson = processProbeInfo(probeInfo)
                    #Agrupa as informações da probe por ID
                    if probeJson['probeId'] in probeGroupedInfo:
                        probeGroupedInfo[probeJson['probeId']].append(probeJson)
                    else:
                        probeGroupedInfo[probeJson['probeId']] = [probeJson]
            
            #Itera sobre cada grupo de probes
            for id, data in probeGroupedInfo.items():
                rows = []
                #Itera sobre cada medição da probe
                for measurement in data:
                    #Itera sobre cada hop (salto) na medição
                    for hop_num, hop_latencies in enumerate(measurement['latencia'], start=1):
                        if hop_latencies:
                            #Adiciona as latências dos hops às linhas de dados
                            for rtt in hop_latencies:
                                rows.append({
                                    'probe_id': measurement['probeId'],
                                    'destination': measurement['destino'],
                                    'country': measurement['pais'],
                                    'continent': measurement['continente'],
                                    'timestamp': measurement['data'],
                                    'hop': hop_num,
                                    'rtt': rtt
                                })
                #Cria um dataframe com as linhas de dados
                dataframe = pd.DataFrame(rows)
                dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

                #Gerando um diretório para armazenar os gráficos das probes por destino
                output_dir = f'imagensProbes/{dataframe["destination"].iloc[0]}'
                os.makedirs(output_dir, exist_ok=True)
                #Gerando os gráficos de latência, saltos e latência x saltos das probes
                plotLatencyOverTime(dataframe, output_dir, id)
                plotHopsOverTime(dataframe, output_dir, id)
                plotLatencyVsHops(dataframe, output_dir, id)
                #Adiciona as linhas de dados combinadas
                combined_rows.extend(rows)

    #Cria um DataFrame combinado com todas as linhas de dados
    dataframe_combined = pd.DataFrame(combined_rows)
    dataframe_combined['timestamp'] = pd.to_datetime(dataframe_combined['timestamp'])

    #Gráficos por continente e por destino
    for destination in dataframe_combined['destination'].unique():

        #Filtra os dados para o destino atual
        dataframe_destination = dataframe_combined[dataframe_combined['destination'] == destination]
        
        
        for continent in dataframe_destination['continent'].unique():
            #Filtra os dados para o continente atual
            dataframe_continent = dataframe_destination[dataframe_destination['continent'] == continent]
            #Agrupa os dados por hora
            dataframe_hourly_combined_continent = dataframe_continent.groupby(['continent', pd.Grouper(key='timestamp', freq='H')]).agg({
                'rtt': 'mean',
                'hop': 'mean'
            }).reset_index()

            #Cria um diretório para o continente atual dentro do diretório de destinos
            output_dir = f'imagensContinentes/{destination}/{continent}'
            os.makedirs(output_dir, exist_ok=True)

            #Gera os gráficos de latência, saltos e relação latência x saltos por continente
            plotLatencyOverTimeByContinent(dataframe_hourly_combined_continent, output_dir)
            plotHopsOverTimeByContinent(dataframe_hourly_combined_continent, output_dir)
            plotLatencyVsHopsByContinent(dataframe_continent, output_dir)
        #Gera gráficos comparativos de todos os continentes para o destino atual
        output_dir = f'imagensContinentes/{destination}'
        os.makedirs(output_dir, exist_ok=True)
        plotLatencyOverTimeByContinent(dataframe_destination, output_dir)
        plotHopsOverTimeByContinent(dataframe_destination, output_dir)
        plotLatencyVsHopsByContinent(dataframe_destination, output_dir)
        
    
    #Gráficos por país e por destino
    for destination in dataframe_combined['destination'].unique():
        #Filtra os dados para o destino atual
        dataframe_destination = dataframe_combined[dataframe_combined['destination'] == destination]
        
        for country in dataframe_destination['country'].unique():
            #Filtra os dados para o país atual
            dataframe_country = dataframe_destination[dataframe_destination['country'] == country]
            #Agrupa os dados por hora
            dataframe_hourly_combined_country = dataframe_country.groupby(['country', pd.Grouper(key='timestamp', freq='H')]).agg({
                'rtt': 'mean',
                'hop': 'mean'
            }).reset_index()

            #Cria um diretório para o país atual dentro do diretório de destinos
            output_dir = f'imagensPaises/{destination}/{country}'
            os.makedirs(output_dir, exist_ok=True)

            #Gera os gráficos de latência, saltos e relação latência x saltos por país
            plotLatencyOverTimeByCountry(dataframe_hourly_combined_country, output_dir)
            plotHopsOverTimeByCountry(dataframe_hourly_combined_country, output_dir)
            plotLatencyVsHopsByCountry(dataframe_country, output_dir)
        #Gera gráficos comparativos de todos os países para o destino atual
        output_dir = f'imagensPaises/{destination}'
        os.makedirs(output_dir, exist_ok=True)
        plotLatencyOverTimeByCountry(dataframe_destination, output_dir)
        plotHopsOverTimeByCountry(dataframe_destination, output_dir)
        plotLatencyVsHopsByCountry(dataframe_destination, output_dir)

    #Agrupa os dados por destino e hora
    dataframe_hourly_combined_destination = dataframe_combined.groupby(['destination', pd.Grouper(key='timestamp', freq='H')]).agg({
        'rtt': 'mean',
        'hop': 'mean'
    }).reset_index()

    #Cria um diretório para os gráficos por destino
    output_dir = 'imagensDestinos'
    os.makedirs(output_dir, exist_ok=True)

    #Gera os gráficos de latência e saltos por destino
    plotLatencyOverTimeByDestination(dataframe_hourly_combined_destination, output_dir)
    plotHopsOverTimeByDestination(dataframe_hourly_combined_destination, output_dir)
    plotLatencyVsHopsByDestination(dataframe_combined, output_dir)

if __name__ == "__main__":
    main()
