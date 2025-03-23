Feature: Validação da Infraestrutura AWS no LocalStack

  Scenario: Verificar criação de bucket S3
    Given que o bucket "meu-bucket" não existe
    When eu crio o bucket "meu-bucket"
    Then o bucket "meu-bucket" deve existir

  Scenario: Verificar criação de tabela DynamoDB
    Given que a tabela "minha-tabela" não existe
    When eu crio a tabela "minha-tabela" com chave primária "ID"
    Then a tabela "minha-tabela" deve existir com a chave primária "ID"
