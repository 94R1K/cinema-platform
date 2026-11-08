-- Получаем параметры текущего сервиса
\getenv db_name DB_NAME
\getenv db_user DB_USER
\getenv db_password DB_PASSWORD


-- Создаем роль, если она отсутствует
SELECT format(
    'CREATE ROLE %I WITH LOGIN PASSWORD %L',
    :'db_user',
    :'db_password'
)
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_roles
    WHERE rolname = :'db_user'
)
\gexec


-- Создаем базу данных, если она отсутствует
SELECT format(
    'CREATE DATABASE %I OWNER %I',
    :'db_name',
    :'db_user'
)
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = :'db_name'
)
\gexec


-- Обеспечиваем правильного владельца
SELECT format(
    'ALTER DATABASE %I OWNER TO %I',
    :'db_name',
    :'db_user'
)
\gexec


-- Запрещаем публичный доступ
SELECT format(
    'REVOKE ALL ON DATABASE %I FROM PUBLIC',
    :'db_name'
)
\gexec
