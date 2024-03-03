show databases;
create database extensao;
use extensao;

CREATE TABLE Trabalhador (
    idCPF CHAR(11) NOT NULL PRIMARY KEY,
    Email VARCHAR(40) NOT NULL,
    Nome VARCHAR(40) NOT NULL,
    Bairro VARCHAR(25) NOT NULL,
    Serviço VARCHAR(30) NOT NULL,
    Contato VARCHAR(12) NOT NULL,
    Senha_hash VARCHAR(255) NOT NULL
);

CREATE TABLE Usuário (
    idCPF CHAR(11) NOT NULL PRIMARY KEY,
    Email VARCHAR(40) NOT NULL,
    Nome VARCHAR(40) NOT NULL,
    Endereço VARCHAR(255) NOT NULL,
    Bairro VARCHAR(25) NOT NULL,
    Senha_hash VARCHAR(255) NOT NULL
);
