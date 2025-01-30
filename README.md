# Email Classifier

Este projeto é uma aplicação para classificar emails como produtivos ou improdutivos e sugerir respostas utilizando modelos de NLP.

## Requisitos

- Python 3.8+
- pip (Python package installer)

## Instalação

1. Clone o repositório:
    
    git clone https://github.com/joaoadn/AutoU-Practical-Case-Project.git
    cd AutoU-Practical-Case-Project
    

2. Crie um ambiente virtual:
    
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    

3. Instale as dependências:
    
    pip install -r requirements.txt
    

## Configuração

1. Crie um arquivo `.env` na raiz do projeto e adicione suas chaves de API:
    
    OPENAI_API_KEY=your_openai_api_key
    

## Execução

1. Execute o servidor Flask:
    
    flask run
    

2. Acesse a aplicação no navegador:
    
    http://127.0.0.1:5000
    

## Testes

1. Para executar os testes unitários, use:
    
    python -m unittest discover -s tests
    

## Estrutura do Projeto

.
├── src
│   ├── app.py
│   ├── prepare_training_data.py
│   ├── train_model.py
│   ├── downloadmodel.py
│   └── ...
├── static
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── tests
│   └── test_app.py
├── .env
├── requirements.txt
└── README.md