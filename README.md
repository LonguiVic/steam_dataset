```
data_pipeline_project/
│
├── config/                    
│   ├── api_config.yaml
│
├── data/                       # Dados brutos, processados, e de saída
│   ├── raw/                    # Dados brutos extraídos
│   ├── processed/              # Dados tratados (parciais ou limpos)
│   └── output/                 # Dados prontos para consumo ou carga
│
├── extract/                    # Código de extração de diferentes fontes
│   ├── api/
│       └── steam_extractor.py
│
├── utils/                      # Funções utilitárias (logs, handlers, helpers)
│   ├── logger.py
│   ├── api_handler.py
│
├── tests/                      # Testes unitários e de integração
│   ├── test_extract.py
│
├── logs/
│
├── main.py                     # Script principal / entrypoint
├── .env                    # Configurações como `.env`, arquivos YAML ou JSON
└── README.md                # Documentação do projeto
```


# input steam:

1- Quem são os TOP N (N sendo quantidade de jogos) mais jogados:
    1.1- Testar webscrapping na Steam e na SteamDB
    1.2- Pegar a lista de AppIds do TOP N

2 - Fazer webscrapping para gerar o dataset 1

3 - Fazer requisição da API pra gerar o dataset 2 

# outputs steam:

primeira extração:
nome (appids) dos jogos mais jogados do dia


dataset 1:
APPID | NOME DO JOGO | PREÇO DO JOGO | JOGADORES AGORA | FREE (BOOLEAN) |  PICO DIARIO <----- {WEBSCRAPPING}

dataset 2:
IdREVIEW | APPID | NOME | MSG | RECOMENDADO (BOOLEAN) | USUARIO DO REVIEWER | HORAS JOGADAS | COUNTRY <----- {API DA STEAM}



## Exemplo de review:
```json
{
    "recommendationid": "195071834",
    "author": {
        "steamid": "76561199237111259",
        "num_games_owned": 54,
        "num_reviews": 13,
        "playtime_forever": 9711,
        "playtime_last_two_weeks": 662,
        "playtime_at_review": 9473,
        "last_played": 1747602542
    },
    "language": "english",
    "review": "lot of hacker, i que for mirage all the time, 13 rounds in a row i play against hackers, i can't take it enymore. VAC is the biggest ********",
    "timestamp_created": 1747486247,
    "timestamp_updated": 1747486247,
    "voted_up": false,
    "votes_up": 4,
    "votes_funny": 0,
    "weighted_vote_score": "0.555690288543701172",
    "comment_count": 0,
    "steam_purchase": true,
    "received_for_free": false,
    "written_during_early_access": false,
    "primarily_steam_deck": false
}
```