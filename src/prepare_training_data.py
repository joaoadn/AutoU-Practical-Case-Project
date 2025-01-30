import pandas as pd
import os
import re

# Caminho para salvar o arquivo CSV
output_path = "../data/email_training_data.csv"  # Caminho relativo à pasta `src/`

# Verifica se a pasta de dados existe, caso contrário, cria
if not os.path.exists(os.path.dirname(output_path)):
    os.makedirs(os.path.dirname(output_path))

# Função para limpar e normalizar o texto
def clean_text(text):
    text = text.lower()  # Converte para minúsculas
    text = re.sub(r'\d+', '', text)  # Remove números
    text = re.sub(r'\s+', ' ', text)  # Remove espaços extras
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
    return text

# Dados de exemplo para treinamento
training_data = {
    'text': [
        # Emails Produtivos
        "Preciso de suporte técnico urgente. O sistema está fora do ar desde às 14h.",
        "Por favor, pode me ajudar com o erro #1234 que está aparecendo no módulo de relatórios?",
        "Solicito atualização sobre o caso #5678 aberto na semana passada.",
        "O sistema está apresentando lentidão. Necessito de verificação urgente.",
        "Não consigo acessar minha conta. Preciso de ajuda para resetar a senha.",
        "Encontrei um bug no módulo de exportação. Podem verificar?",
        "Precisamos agendar uma reunião para discutir as atualizações do sistema.",
        "Solicitação de novo acesso para o usuário João Silva.",
        "Bug crítico identificado na última atualização. Necessita correção imediata.",
        "Relatório mensal apresentando inconsistências. Requer análise.",
        # Adicione mais exemplos de emails produtivos aqui...
        
        # Emails Improdutivos
        "Obrigado pela ajuda com o sistema ontem!",
        "Desejo a todos um ótimo feriado!",
        "Parabéns pelo excelente trabalho realizado!",
        "Recebi o relatório, muito obrigado.",
        "Confirmando o recebimento do email anterior.",
        "Ótimo trabalho na apresentação de hoje!",
        "Feliz aniversário! Desejo tudo de bom.",
        "Agradecendo a atenção de sempre.",
        "Newsletter mensal da empresa.",
        "Convite para happy hour da equipe."
        # Adicione mais exemplos de emails improdutivos aqui...
    ],
    'label': [
        # Labels correspondentes (1 para Produtivo, 0 para Improdutivo)
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
}

# Limpar e normalizar os textos
training_data['text'] = [clean_text(text) for text in training_data['text']]

# Criar DataFrame
df = pd.DataFrame(training_data)

# Salvar como CSV
df.to_csv(output_path, index=False)