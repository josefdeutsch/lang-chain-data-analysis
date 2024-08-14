statistics
│
├── analytics
│   ├── src
│   │   ├── timeseries
│   │   ├── entrypoint.sh
│   │   ├── main.py
│   ├── Dockerfile
│   └── pyproject.toml
│
├── chat_api
│   ├── src
│   │   ├── agents
│   │   │   └── chat_api_agent.py
│   │   ├── chains
│   │   │   └── stock_cypher_chain.py
│   │   ├── models
│   │   ├── tools
│   │   │   ├── math
│   │   │   │   ├── stat.py
│   │   │   │   └── wrapper.py
│   │   ├── utils
│   │   ├── entrypoint.sh
│   │   └── main.py
│   ├── Dockerfile
│   ├── .gitignore
│   └── pyproject.toml
│
├── chat_bot
│   ├── src
│   │   ├── entrypoint.sh
│   │   └── main.py
│   ├── .gitignore
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── README.md
│   └── data
│
├── neo4j_etl
│   ├── src
│   │   ├── entrypoint.sh
│   │   ├── main.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── .gitignore
│
├── neo4j-docker-setup
│   ├── plugins
│   │   ├── apoc-5.1.0-core.jar
│   │   ├── apoc-5.1.0-extended.jar
│   └── Dockerfile
│
├── data
│
├── .gitignore
│
├── docker-compose.yml
│
├── README.md
│
└── requirements.txt
