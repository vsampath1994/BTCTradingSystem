-- CS 6360 Final Project SQL (Part II)
-- Michael Holcomb (mjh170630)
-- Harshavardhan Nalajala (hxn170230)
-- Vigneshwaran Sampath (vxs180021)
drop database if exists bitcoinmanagement_test;
CREATE USER 'sql_admin'@'localhost' IDENTIFIED BY 'progamut';
GRANT ALL PRIVILEGES ON bitcoinmanagement_test . * TO 'sql_admin'@'localhost';
create database bitcoinmanagement_test;
use bitcoinmanagement_test;
create table users(
	id int(11) UNIQUE AUTO_INCREMENT,
	username varchar(255) UNIQUE,
	password_hash varchar(255),
	btc_balance float,
	cell_number varchar(255),
	city varchar(255),
	email varchar(255) UNIQUE,
	fiat_balance float,
	first_name varchar(255),
	last_name varchar(255),
	gold_status tinyint(1),
	phone_number varchar(255),
	street varchar(255),
	state varchar(255),
	user_type tinyint(1) NOT NULL,
	zip_code varchar(255),
	PRIMARY KEY(id)
);

create table payments(
	xid int(11) UNIQUE NOT NULL AUTO_INCREMENT,
	status varchar(255) NOT NULL,
	fiatAmount float NOT NULL,
	clientId int(11) NOT NULL,
	traderId int(11) NOT NULL,
	timestamp datetime NOT NULL,
	PRIMARY KEY (xid)
);

create table orders(
	xid int(11) UNIQUE NOT NULL AUTO_INCREMENT,
	status varchar(255) NOT NULL,
	isBuy tinyint(1) NOT NULL,
	btc_amount float NOT NULL,
	xchange float,
	comm_type varchar(255) NOT NULL,
	comm_amount float NOT NULL,
	clientId int(11),
	traderId int(11),
	timestamp datetime NOT NULL,
	PRIMARY KEY(xid)
);

create table changelog(
	lid int(11) UNIQUE NOT NULL AUTO_INCREMENT,
	timestamp datetime NOT NULL,
	xid int(11) NOT NULL,
	clientId int(11),
	traderId int(11),
	status varchar(255) NOT NULL,
	xid_type varchar(255) NOT NULL,
	PRIMARY KEY(lid)
);

select * from users;

delimiter $$
create procedure add_clients_traders()
begin
	declare id int;
	set id = 1;
	while id <= 100 do
		insert into users values(id, concat('client', id), 'pbkdf2:sha256:50000$DkK7IZln$2684320e81bc641b2329c1bfe66370e9ca10b823d35077a9a543ed2ae021be66', 10, concat('469422929', id), 'Dallas', concat('first', id, 'last.com'), 40000, concat('client', id), concat('clientlast', id), 0, concat('469422929', id), concat('7421 Frank', id), 'Texas', 2, concat('7525' , id));
		insert into users values(id+1000, concat('trader', id+1000), 'pbkdf2:sha256:50000$DkK7IZln$2684320e81bc641b2329c1bfe66370e9ca10b823d35077a9a543ed2ae021be66', 10, concat('469422929', id+1000), 'Dallas', concat('first', id+1000, 'last.com'), 40000, concat('trader', id+1000), concat('traderlast', id+1000), 0, concat('469422929', id+1000), concat('7421 Frank', id+1000), 'Texas', 3, concat('7525' , id+1000));
		set id = id + 1;
	end while;
end; $$

create procedure add_payment_order() 
begin  
	declare id int; 
	declare time datetime;
	set time = '2011-09-01 15:00:00';
	set id = 3;
	while id <= 2600 do
		insert into payments values(id, 'pending', 1000, MOD(id,100), MOD((id+23),100), ADDTIME(time, "23:00:00.00"));
		insert into changelog values(id, ADDTIME(time, "23:00:00.00"), id, MOD(id,100), NULL,'pending', 'Deposit');
		insert into payments values(id+10000, 'completed', 500, MOD(id,100), (id+37)%100 + 1000, ADDTIME(time, "12:00:00.00"));
		insert into changelog values(id+10000, ADDTIME(time, "12:00:00.00"), id+10000, MOD(id,100), (id+37)%100 + 1000,'completed', 'Deposit');
		insert into orders values(id, 'pending', 0, 10, 4153, 'Bitcoins', 2, MOD(id,100), NULL, ADDTIME(time, "10:00:00.00"));
		insert into changelog values(id+20000, ADDTIME(time, "10:00:00.00"), id, MOD(id,100), NULL,'pending', 'Order');
		insert into orders values(id+10000, 'completed', 0, 10, 4672, 'Bitcoins', 2, MOD(id,100), MOD((id+37),100) + 1000, ADDTIME(time, "12:00:00.00"));
		insert into changelog values(id+30000, ADDTIME(time, "12:00:00.00"), id+10000, MOD(id,100), (id+37)%100 + 1000,'completed', 'Order');
		insert into orders values(id+20000, 'pending', 1, 500, 4500, 'Fiat', 100, MOD(id,100), NULL, ADDTIME(time, "06:00:00.00"));
		insert into changelog values(id+40000, ADDTIME(time, "06:00:00.00"), id+20000, MOD(id,100), NULL,'pending', 'Order');
		insert into orders values(id+30000, 'completed', 1, 10, 4859, 'Fiat', 100, MOD(id,100), MOD((id+23),100) + 1000, ADDTIME(time, "04:00:00.00"));
		insert into changelog values(id+50000, ADDTIME(time, "04:00:00.00"), id+30000, MOD(id,100), (id+23)%100 + 1000,'completed', 'Order');
		set id = id + 1;
		set time = ADDDATE(time, 1);
        end while; 
end; $$

create procedure add_client_trade()
begin
	declare id int;
	declare time datetime;
	set id = 1;
	set time = NOW();
	insert into orders values(id+65000, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65000, NOW(), id+65000, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65001, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65001, NOW(), id+65001, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65002, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65002, NOW(), id+65002, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65003, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65003, NOW(), id+65003, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65004, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65004, NOW(), id+65004, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65005, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65005, NOW(), id+65005, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65006, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65006, NOW(), id+65006, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65007, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65007, NOW(), id+65007, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65008, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65008, NOW(), id+65008, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65009, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65009, NOW(), id+65009, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65010, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65010, NOW(), id+65010, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65011, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65011, NOW(), id+65011, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65012, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65012, NOW(), id+65012, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65013, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65013, NOW(), id+65013, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65014, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65014, NOW(), id+65014, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65015, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65015, NOW(), id+65015, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65016, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65016, NOW(), id+65016, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65017, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65017, NOW(), id+65017, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65018, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65018, NOW(), id+65018, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65019, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65019, NOW(), id+65019, 1, 10001, 'completed', 'Order');
	insert into orders values(id+65020, 'completed', 1, 500, 4500, 'Fiat', 100, 1, 1001, NOW());
	insert into changelog values(id+65020, NOW(), id+65020, 1, 10001, 'completed', 'Order');
end; $$

delimiter ;
call add_clients_traders();
call add_payment_order();
call add_client_trade();
