import pandas as pd

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
    ],
    'label': [
        # Labels correspondentes (1 para Produtivo, 0 para Improdutivo)
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
}

# Criar DataFrame
df = pd.DataFrame(training_data)

# Salvar como CSV
df.to_csv('email_training_data.csv', index=False)
print("Dados de treinamento salvos em email_training_data.csv")