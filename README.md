## Email Classifier

## Visão Geral

Este projeto consiste em uma solução digital para classificação automatizada de emails em uma grande empresa do setor financeiro. A aplicação utiliza inteligência artificial e processamento de linguagem natural (NLP) para:

Classificar emails como produtivos ou improdutivos.

Sugerir respostas automáticas com base no teor da mensagem.

Essa automação permite que a equipe economize tempo, evitando a necessidade de triagem manual dos emails.

## Funcionalidades

1. Classificação de Emails

Os emails serão classificados em duas categorias principais:

Produtivo: Mensagens que requerem uma ação ou resposta (ex.: solicitações de suporte, atualizações sobre casos em aberto, dúvidas técnicas).

Improdutivo: Mensagens sem necessidade de ação imediata (ex.: felicitações, agradecimentos).

2. Sugestão de Respostas Automáticas

Com base na classificação, a aplicação gera uma resposta sugerida para cada email.

3. Interface Web

Upload de Arquivos: Suporte para arquivos .txt e .pdf, além da opção de inserir texto diretamente.

Exibição dos Resultados: Apresenta a classificação do email e a resposta sugerida.

4. Backend em Python

Processamento de Linguagem Natural (NLP): Remoção de stop words, stemming/lemmatização, entre outros.

Modelos de IA: Uso de OpenAI API e um modelo treinado com BERT em português para classificação e geração de respostas.

Integração Backend-Frontend: Conexão entre a API e a interface web para interação dinâmica.

5. Deploy na Nuvem

Hospedagem: Implementação realizada na Vercel.

Disponibilidade Online: Um link funcional será fornecido para acesso externo.

## Instalação e Configuração

1. Clonar o Repositório

git clone https://github.com/joaoadn/AutoU-Practical-Case-Project.git
cd AutoU-Practical-Case-Project

## 2. Criar um Ambiente Virtual

python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`

## 3. Instalar Dependências

pip install -r requirements.txt

## 4. Configurar Chaves de API

Crie um arquivo .env na raiz do projeto e adicione:

OPENAI_API_KEY=your_openai_api_key

## 5. Executar a Aplicação

python app.py

## Acesse a interface web no navegador:

http://127.0.0.1:5000

## Testes

Executar Testes Unitários

python -m unittest discover -s tests

Contribuição

Ficamos felizes em receber contribuições! Siga os passos:

Faça um fork do repositório.

Crie um branch para sua funcionalidade (git checkout -b minha-feature).

Faça commit das suas alterações (git commit -m 'Adiciona nova funcionalidade').

Envie as alterações (git push origin minha-feature).

Abra um Pull Request.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Contato

Caso tenha dúvidas ou sugestões, entre em contato:

Email: joaoadn@outlook.com

LinkedIn: joaoadn


    
