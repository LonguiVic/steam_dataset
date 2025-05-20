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
