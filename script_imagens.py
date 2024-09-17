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

pais = []
cod = []

pais = []
cod = []
probeGroupedInfo = {}

with open('jsonFiles/GoogleNews.json', 'r') as jsonFile:
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
        
        if probeJson['probeId'] in probeGroupedInfo:
            probeGroupedInfo[probeJson['probeId']].append(probeJson['pais'])
        else:
            probeGroupedInfo[probeJson['probeId']] = [probeJson['pais']]

for x in probeGroupedInfo:
    if x not in cod:
        cod.append(x)
        pais.append(probeGroupedInfo[x][0])
paises = list(set(pais))

output_dir = 'imagens/GoogleNews'

for pais in paises:
    probeGroupedInfo = {}
    with open('jsonFiles/GoogleNews.json', 'r') as jsonFile:
        resultInfo = json.load(jsonFile)
    for probeInfo in resultInfo['info']:
        if probeInfo["destination_ip_responded"] and getProbeCountry(probeInfo['prb_id']) == pais: 
            probeJson = {
                'probeId': probeInfo['prb_id'],
                'destino': probeInfo['dst_name'],
                'pais': getProbeCountry(probeInfo['prb_id']),
                'continente': getProbeContinent(probeInfo['prb_id']),
                'latencia': getLatency(probeInfo),
                'quantidadeSaltos': len(probeInfo['result']),
                'data': datetime.fromtimestamp(probeInfo['stored_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if probeJson['probeId'] in probeGroupedInfo:
                probeGroupedInfo[probeJson['probeId']].append(probeJson)
            else:
                probeGroupedInfo[probeJson['probeId']] = [probeJson]
    ids = [x for x in probeGroupedInfo]

    #id seria o id da probe
    for id in ids:
        data = probeGroupedInfo[id]

        rows = []

        # Iterar sobre cada medição
        for measurement in data:
            probe_id = measurement['probeId']
            destination = measurement['destino']
            country = measurement['pais']
            continent = measurement['continente']
            timestamp = measurement['data']
            
            for hop_num, hop_latencies in enumerate(measurement['latencia'], start=1):
                # Ignorar saltos vazios
                if hop_latencies:
                    for rtt in hop_latencies:
                        rows.append({
                            'probe_id': probe_id,
                            'destination': destination,
                            'country': country,
                            'continent': continent,
                            'timestamp': timestamp,
                            'hop': hop_num,
                            'rtt': rtt
                        })

        # Criar o DataFrame
        df = pd.DataFrame(rows)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Plotar a variação da latência ao longo do tempo por destino
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=df, x='timestamp', y='rtt', hue='destination', marker='o', errorbar=None)
        plt.title('Variação da Latência ao Longo do Tempo por probe')
        plt.xlabel('Tempo')
        plt.ylabel('Latência (ms)')
        plt.legend(title='Destino', loc='upper right')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'latencia_por_tempo_{id}.png'))
        plt.show()


        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns

        data = probeGroupedInfo[id]  # de 0 a 3 qual probe por país você quer

        rows = []

        # Iterar sobre cada medição
        for measurement in data:
            probe_id = measurement['probeId']
            destination = measurement['destino']
            country = measurement['pais']
            continent = measurement['continente']
            timestamp = measurement['data']
            
            for hop_num, hop_latencies in enumerate(measurement['latencia'], start=1):
                # Ignorar saltos vazios
                if hop_latencies:
                    for rtt in hop_latencies:
                        rows.append({
                            'probe_id': probe_id,
                            'destination': destination,
                            'country': country,
                            'continent': continent,
                            'timestamp': timestamp,
                            'hop': hop_num
                        })

        # Criar o DataFrame
        df = pd.DataFrame(rows)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Plotar a variação da quantidade de saltos ao longo do tempo por destino
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=df, x='timestamp', y='hop', hue='destination', marker='o', errorbar=None)
        plt.title('Variação da Quantidade de Saltos ao Longo do Tempo por probe')
        plt.xlabel('Tempo')
        plt.ylabel('Quantidade de Saltos')
        plt.legend(title='Destino', loc='upper right')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'saltos_por_tempo_{id}.png'))
        plt.show()

        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns

        data = probeGroupedInfo[ids[1]]  # de 0 a 3 qual probe por país você quer

        rows = []

        # Iterar sobre cada medição
        for measurement in data:
            probe_id = measurement['probeId']
            destination = measurement['destino']
            country = measurement['pais']
            continent = measurement['continente']
            timestamp = measurement['data']
            
            for hop_num, hop_latencies in enumerate(measurement['latencia'], start=1):
                # Ignorar saltos vazios
                if hop_latencies:
                    for rtt in hop_latencies:
                        rows.append({
                            'probe_id': probe_id,
                            'destination': destination,
                            'country': country,
                            'continent': continent,
                            'timestamp': timestamp,
                            'hop': hop_num,
                            'rtt': rtt
                        })

        # Criar o DataFrame
        df = pd.DataFrame(rows)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Plotar a relação entre latência e quantidade de saltos
        plt.figure(figsize=(12, 8))
        sns.scatterplot(data=df, x='hop', y='rtt', hue='destination', marker='o')
        plt.title('Relação entre Latência e Quantidade de Saltos')
        plt.xlabel('Quantidade de Saltos')
        plt.ylabel('Latência (ms)')
        plt.legend(title='Destino', loc='upper right')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'latencia_X_saltos{id}.png'))
        plt.show()
