# Ripe Atlas Measurements <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWt4cm5wczhxMmR4MGZpeWFwaGEwNWNyMjlrMjRtc2x3ZTBhdnFqZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/Tfd91e9R13cewUzBWh/giphy.gif" width="55"/>

Este projeto realiza a análise de latência de probes a partir de dados fornecidos em arquivos JSON. O pipeline desenvolvido carrega os dados, processa as informações relevantes, gera gráficos de latência e quantidade de saltos, e organiza os gráficos em diretórios específicos por destino, continente e país.

## Estrutura do Projeto

- `jsonFiles/`: Diretório contendo os arquivos JSON com os dados das probes.
- `imagensProbes/`: Diretório contendo gráficos de cada probe, organizados por destino.
- `imagensContinentes/`: Diretório contendo gráficos por continente, organizados por destino.
- `imagensPaises/`: Diretório contendo gráficos por país, organizados por destino.
- `imagensDestinos/`: Diretório contendo gráficos por destino.
- `probesLocation.py`: Script contendo o dicionário `probesLocation` com informações de localização das probes.
- `main.py`: Script principal que executa o pipeline de análise.

## Instalação

1. Clone o repositório para o seu ambiente local:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

## Bibliotecas Utilizadas

- `pandas`: Para manipulação e análise de dados.
- `matplotlib`: Para criação de gráficos.
- `seaborn`: Para visualização de dados estatísticos.
- `json`: Para manipulação de dados JSON.
- `datetime`: Para manipulação de datas e horas.
- `os`: Para manipulação de diretórios e arquivos.

## Execução

1. Certifique-se de que os arquivos JSON com os dados das probes estão no diretório `jsonFiles/`.
2. Execute o script principal:
    ```bash
    python main.py
    ```

## Estrutura de Diretórios

- **imagensProbes**: Contém gráficos de cada probe, organizados por destino.
- **imagensContinentes**: Contém gráficos por continente, organizados por destino.
- **imagensPaises**: Contém gráficos por país, organizados por destino.
- **imagensDestinos**: Contém gráficos por destino.

## Descrição do Pipeline

1. **Carregamento de Dados**:
   - Os dados são carregados a partir dos arquivos JSON e armazenados em um DataFrame.

2. **Processamento de Dados**:
   - As probes são agrupadas por país com base no ID da probe.
   - Para cada probe, são extraídas informações relevantes, como ID da probe, destino, país, continente, latência e quantidade de saltos.

3. **Geração de Gráficos para Probes**:
   - Diretórios específicos são criados para armazenar os gráficos das probes, organizados por destino.
   - São gerados gráficos de latência ao longo do tempo, quantidade de saltos ao longo do tempo e relação entre latência e quantidade de saltos para cada probe.

4. **Combinação de Dados**:
   - As linhas de dados de todas as probes são combinadas em um único DataFrame.

5. **Geração de Gráficos por Continente e Destino**:
   - Os dados são filtrados por continente para cada destino.
   - Os dados são agrupados por hora para calcular a média de latência e quantidade de saltos.
   - Diretórios específicos são criados para armazenar os gráficos por continente, organizados por destino.
   - São gerados gráficos de latência ao longo do tempo, quantidade de saltos ao longo do tempo e relação entre latência e quantidade de saltos para cada continente.

6. **Geração de Gráficos por País e Destino**:
   - Os dados são filtrados por país para cada destino.
   - Os dados são agrupados por hora para calcular a média de latência e quantidade de saltos.
   - Diretórios específicos são criados para armazenar os gráficos por país, organizados por destino.
   - São gerados gráficos de latência ao longo do tempo, quantidade de saltos ao longo do tempo e relação entre latência e quantidade de saltos para cada país.

7. **Geração de Gráficos por Destino**:
   - Os dados são agrupados por hora para calcular a média de latência e quantidade de saltos.
   - Um diretório específico é criado para armazenar os gráficos por destino.
   - São gerados gráficos de latência ao longo do tempo, quantidade de saltos ao longo do tempo e relação entre latência e quantidade de saltos para cada destino.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias e correções.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
