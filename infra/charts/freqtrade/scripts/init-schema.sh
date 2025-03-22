#!/bin/bash
set -e

# Este script verifica se o schema do cliente existe e o cria se necessário
# Utiliza a variável de ambiente CLIENT_SCHEMA para determinar o schema a ser criado

# Valida se as variáveis necessárias estão definidas
if [ -z "$DATABASE_URL" ]; then
  echo "ERRO: Variável DATABASE_URL não definida"
  exit 1
fi

if [ -z "$CLIENT_SCHEMA" ]; then
  echo "ERRO: Variável CLIENT_SCHEMA não definida"
  exit 1
fi

echo "Verificando existência do schema $CLIENT_SCHEMA..."

# Extrai as credenciais da DATABASE_URL
DB_USER=$(echo $DATABASE_URL | sed -n 's/^postgresql:\/\/\([^:]*\):.*/\1/p')
DB_PASSWORD=$(echo $DATABASE_URL | sed -n 's/^postgresql:\/\/[^:]*:\([^@]*\)@.*/\1/p')
DB_HOST=$(echo $DATABASE_URL | sed -n 's/^postgresql:\/\/[^:]*:[^@]*@\([^:]*\):.*/\1/p')
DB_PORT=$(echo $DATABASE_URL | sed -n 's/^postgresql:\/\/[^:]*:[^@]*@[^:]*:\([^/]*\)\/.*/\1/p')
DB_NAME=$(echo $DATABASE_URL | sed -n 's/^postgresql:\/\/[^:]*:[^@]*@[^:]*:[^/]*\/\([^?]*\).*/\1/p')

# Verifica se o schema existe e o cria se necessário
export PGPASSWORD=$DB_PASSWORD
SCHEMA_EXISTS=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name = '$CLIENT_SCHEMA';")

if [ -z "$SCHEMA_EXISTS" ]; then
  echo "Schema $CLIENT_SCHEMA não existe. Criando..."
  psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "CREATE SCHEMA $CLIENT_SCHEMA;"
  echo "Schema $CLIENT_SCHEMA criado com sucesso."
  
  # Garantir que o usuário tem acesso ao schema
  psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "GRANT ALL ON SCHEMA $CLIENT_SCHEMA TO $DB_USER;"
  echo "Permissões concedidas ao usuário $DB_USER no schema $CLIENT_SCHEMA."
  
  # Criar tabelas do Freqtrade no schema específico do cliente
  # Nota: O Freqtrade normalmente cria as tabelas automaticamente
  # Mas podemos garantir que o schema está configurado corretamente
  echo "Configurando search_path para $CLIENT_SCHEMA..."
  psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "ALTER ROLE $DB_USER SET search_path TO $CLIENT_SCHEMA, public;"
else
  echo "Schema $CLIENT_SCHEMA já existe."
fi

echo "Inicialização do schema concluída."
exit 0
