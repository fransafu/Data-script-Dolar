drop database if exists Monedas;

-- No se que nombre ponerle :P
create database Monedas;
use Monedas;

create table Dolar
( idDollar int not null auto_increment primary key,
  Fecha date,
  Valor varchar(16) );
