drop database if exists Divisas;

create database Divisas;

use Divisas;

create table Dolar
( idDolar int not null auto_increment primary key,
  Fecha date,
  Valor float );
