import json
from datetime import datetime
from probesLocation import probesLocation
import matplotlib.pyplot as plt
import pandas as pd

def getProbeCountry(probeId):  # pegar país
    return probesLocation.get(probeId, {}).get('país', f'ID {probeId} não encontrado')

def getProbeContinent(probeId):  # pegar continente
    return probesLocation.get(probeId, {}).get('continente', f'ID {probeId} não encontrado')

def getLatency(probeInfo):
    latencias = []
    for hop in probeInfo['result']:
        latenciasHop = [item['rtt'] for item in hop['result'] if 'rtt' in item]
        latencias.append(latenciasHop)
    
    return latencias

# Pegar dados relevantes das medições e agrupar por probeId:
def getRelevantInfo(fileName):
    with open(fileName, 'r') as jsonFile:
        resultInfo = json.load(jsonFile)
    for probeInfo in resultInfo['info']:
        if probeInfo["destination_ip_responded"]:  # Verifica se a probe chegou ao destino
            probeJson = {
                'probeId': probeInfo['prb_id'],
                'destino': probeInfo['dst_name'],
                'pais': getProbeCountry(probeInfo['prb_id']),
                'continente': getProbeContinent(probeInfo['prb_id']),
                'latencia': getLatency(probeInfo),
                'quantidadeSaltos': len(probeInfo['result']),
                'data': datetime.fromtimestamp(probeInfo['stored_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Se o probeId já existir no dicionário, adiciona a nova medição à lista existente
            if probeJson['probeId'] in probeGroupedInfo:
                probeGroupedInfo[probeJson['probeId']].append(probeJson)
            else:
                probeGroupedInfo[probeJson['probeId']] = [probeJson]

# Dicionário para armazenar medições agrupadas por probeId
probeGroupedInfo = {}

# Arquivos de exemplo
reuters = 'jsonFiles/Reuters.json'
googleNews = 'jsonFiles/GoogleNews.json'
folhaSP = 'jsonFiles/FolhaSP.json'

# Coleta de informações relevantes
getRelevantInfo(reuters)
getRelevantInfo(googleNews)
getRelevantInfo(folhaSP)

# Exibe as medições agrupadas por probeId
# print(probeGroupedInfo)
# print(f'Total de probes: {len(probeGroupedInfo)}')

#Transformando os dados agrupados por probeId em um DataFrame para facilitar a manipulação
def convert_to_dataframe(probeGroupedInfo):
    data = []
    for probeId, measurements in probeGroupedInfo.items():
        for measurement in measurements:
            for hop_latencies in measurement['latencia']:
                if len(hop_latencies) > 0:
                    latencia_media = sum(hop_latencies) / len(hop_latencies)
                else:
                    latencia_media = None

                data.append({
                    'probeId': probeId,
                    'destino': measurement['destino'],
                    'pais': measurement['pais'],
                    'continente': measurement['continente'],
                    'latencia': latencia_media,
                    'data': measurement['data']
                })
    return pd.DataFrame(data)


df = convert_to_dataframe(probeGroupedInfo)

# Convertendo a coluna 'data' para datetime
df['data'] = pd.to_datetime(df['data'])


#Latência média por destino
def plot_aggregated_latency_by_destination(df):
    df_grouped = df.groupby('destino')['latencia'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(df_grouped['destino'], df_grouped['latencia'])
    
    plt.title('Latência Média para Cada Destino')
    plt.xlabel('Destino')
    plt.ylabel('Latência Média (ms)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#Latência média por continente
def plot_latency_by_continent(df):
    df_grouped = df.groupby('continente')['latencia'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(df_grouped['continente'], df_grouped['latencia'])
    
    plt.title('Latência Média por Continente')
    plt.xlabel('Continente')
    plt.ylabel('Latência Média (ms)')
    plt.tight_layout()
    plt.show()

#Latência média por país
def plot_latency_by_country(df):
    df_grouped = df.groupby('pais')['latencia'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(df_grouped['pais'], df_grouped['latencia'])
    
    plt.title('Latência Média por País')
    plt.xlabel('País')
    plt.ylabel('Latência Média (ms)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Chamar as funções para plotar os gráficos
plot_aggregated_latency_by_destination(df)
plot_latency_by_continent(df)
plot_latency_by_country(df)
