import json
import os

def getProbeCountry(probeId):
    pass
    #pegar o pais do dicionario a partir do id?

def getProbeContinent(probreId):
    pass
    #pegar o continente do dicionario a partir do id?

def getLatency(probeInfo):
    latencias = []
    for hop in probeInfo['result']:
        latencias_hop = [item['rtt'] for item in hop['result'] if 'rtt' in item]
        latencias.append(latencias_hop)
    
    return latencias

file_path = 'jsonFiles/example-probe.json'
if os.path.isfile(file_path):
    print("Arquivo encontrado")
    with open('jsonFiles/example-probe.json', 'r') as jsonFile:
        probeInfo = json.load(jsonFile)

    if (probeInfo["destination_ip_responded"]):
        probeJson = {
            'probeId': probeInfo['prb_id'],
            'pais' : getProbeCountry(probeInfo['prb_id']),
            'continente' : getProbeContinent(probeInfo['prb_id']),
            'latencia' : getLatency(probeInfo),
            'quantidadeSaltos' : len(probeInfo['result'])
        }
        print(probeJson)
    else:
        print(f"Probe {probeInfo['prb_id']} não chegou ao destino")


else:
    print("Arquivo não encontrado")