drop database if exists Divisas;

create database Divisas;

use Divisas;

create table Dolar
( idDolar int not null auto_increment primary key,
  Fecha date not null,
  Valor float not null );

create procedure buscar_fecha(fecha date) 
	select *
    from Dolar d
    where d.Fecha = fecha;


-- `delimiter` cambia el caracter para terminar una sentencia,
-- en este caso lo cambio a `//`

delimiter //
create procedure agregar_fecha(in fecha date, in valor float)
begin
  insert into Dolar (Fecha, Valor) values (fecha, valor);
end //
delimiter ;


delimiter //
create procedure actualizar_fecha(in fecha date, in nuevo_valor float)
begin
	update Dolar
    set Valor = nuevo_valor
    where Dolar.Fecha = fecha;
end //
delimiter ;
