import json
from datetime import datetime
from probesLocation import probesLocation

def getProbeCountry(probeId): #pegar país
    return probesLocation.get(probeId, {}).get('país', f'ID {probeId} não encontrado')

def getProbeContinent(probeId): #pegar continente
    return probesLocation.get(probeId, {}).get('continente', f'ID {probeId} não encontrado')


def getLatency(probeInfo):
    latencias = []
    for hop in probeInfo['result']:
        latenciasHop = [item['rtt'] for item in hop['result'] if 'rtt' in item]
        latencias.append(latenciasHop)
    
    return latencias

#pegar dados relevantes das medições:
def getRelevantInfo(fileName):
    with open(fileName, 'r') as jsonFile:
        resultInfo = json.load(jsonFile)
    for probeInfo in resultInfo['info']:
        if (probeInfo["destination_ip_responded"]): #verifica se a probe chegou ao destino
            probeJson = { #informações de cada probe para gerar os gráficos?
                'probeId': probeInfo['prb_id'],
                'destino' : probeInfo['dst_name'],
                'pais' : getProbeCountry(probeInfo['prb_id']),
                'continente' : getProbeContinent(probeInfo['prb_id']),
                'latencia' : getLatency(probeInfo), #uma lista com a lista de latencias capturadas por salto (hop)
                'quantidadeSaltos' : len(probeInfo['result']),
                'data' : datetime.fromtimestamp(probeInfo['stored_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            }
            probeRelevantInfo.append(probeJson)

#código
probeRelevantInfo = [] #lista pra guardar todos os dados
reuters = 'jsonFiles/Reuters.json'
googleNews = 'jsonFiles/GoogleNews.json'
folhaSP = 'jsonFiles/FolhaSP.json'

getRelevantInfo(reuters)
getRelevantInfo(googleNews)
getRelevantInfo(folhaSP)

#criar gráficos
#percorrer a lista de probeRelevantInfo para usar os dados nos gráficos?
print(probeRelevantInfo)
print(len(probeRelevantInfo))