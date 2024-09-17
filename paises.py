import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
from probesLocation import probesLocation
import os

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

# Carregar os dados JSON
probeGroupedInfo = {}
with open('jsonFiles/GoogleNews.json', 'r') as jsonFile:
    resultInfo = json.load(jsonFile)
    
# Iterar sobre as probes e organizar por país
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
        
        if probeJson['pais'] in probeGroupedInfo:
            probeGroupedInfo[probeJson['pais']].append(probeJson)
        else:
            probeGroupedInfo[probeJson['pais']] = [probeJson]

# Inicializar a lista de dados
rows = []

# Iterar sobre cada país e calcular as médias
for pais, probes in probeGroupedInfo.items():
    for measurement in probes:
        destination = measurement['destino']
        country = measurement['pais']
        continent = measurement['continente']
        timestamp = measurement['data']
        
        for hop_num, hop_latencies in enumerate(measurement['latencia'], start=1):
            if hop_latencies:  # Ignorar saltos vazios
                for rtt in hop_latencies:
                    rows.append({
                        'country': country,
                        'continent': continent,
                        'timestamp': timestamp,
                        'hop': hop_num,
                        'rtt': rtt
                    })

# Criar o DataFrame
df = pd.DataFrame(rows)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Calcular a média da latência e quantidade de saltos por país
df_avg = df.groupby(['country', 'timestamp']).agg({
    'rtt': 'mean',
    'hop': 'mean'
}).reset_index()

# Plotar a média da latência ao longo do tempo por país
plt.figure(figsize=(12, 8))
sns.lineplot(data=df_avg, x='timestamp', y='rtt', hue='country', marker='o')
plt.title('Média da Latência ao Longo do Tempo por País')
plt.xlabel('Tempo')
plt.ylabel('Latência Média (ms)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plotar a média da quantidade de saltos ao longo do tempo por país
plt.figure(figsize=(12, 8))
sns.lineplot(data=df_avg, x='timestamp', y='hop', hue='country', marker='o')
plt.title('Média da Quantidade de Saltos ao Longo do Tempo por País')
plt.xlabel('Tempo')
plt.ylabel('Quantidade Média de Saltos')
plt.grid(True)
plt.tight_layout()
plt.show()
