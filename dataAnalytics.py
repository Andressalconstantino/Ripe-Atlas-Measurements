import json
import os

#funções
def getProbeCountry(probeId):
    pass
    #pegar o pais do dicionario a partir do id?

def getProbeContinent(probreId):
    pass
    #pegar o continente do dicionario a partir do id?

def getLatency(probeInfo):
    latencias = []
    for hop in probeInfo['result']:
        latenciasHop = [item['rtt'] for item in hop['result'] if 'rtt' in item]
        latencias.append(latenciasHop)
    
    return latencias

#código
file_path = 'jsonFiles/example-probe.json'
with open('jsonFiles/example-probe.json', 'r') as jsonFile:
    probeInfo = json.load(jsonFile)

if (probeInfo["destination_ip_responded"]): #verifica se a probe chegou ao destino
    probeJson = { #informações de cada probe para gerar os gráficos?
        'probeId': probeInfo['prb_id'],
        'destino' : probeInfo['dst_name'],
        'pais' : getProbeCountry(probeInfo['prb_id']),
        'continente' : getProbeContinent(probeInfo['prb_id']),
        'latencia' : getLatency(probeInfo),
        'quantidadeSaltos' : len(probeInfo['result'])
    }
    print(probeJson)
else:
    print(f"Probe {probeInfo['prb_id']} não chegou ao destino")