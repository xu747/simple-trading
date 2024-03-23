DROP DATABASE IF EXISTS "simple-trading";
CREATE DATABASE "simple-trading";

\connect "simple-trading"

CREATE TABLE crypto_prices
(
    timestamp   BIGINT,
    symbol      VARCHAR (20),
    price       NUMERIC
);