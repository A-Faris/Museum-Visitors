psql postgres -f schema.sql;

DROP DATABASE IF EXISTS museum;
CREATE DATABASE museum;
\c museum;