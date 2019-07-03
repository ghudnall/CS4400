drop database if exists store;
create database store;
use store;


create table user(
fname varchar(15), 
lname varchar(15), 
username varchar(15) NOT NULL, 
password varchar(15) NOT NULL, 
user_type varchar(15) NOT NULL,
email varchar(25),
PRIMARY KEY(username)
);

create table manager(
username varchar(15) NOT NULL, 
PRIMARY KEY(username),
FOREIGN KEY(username) REFERENCES USER(username)
);

create table deliverer(
username varchar(15) NOT NULL, 
PRIMARY KEY(username),
FOREIGN KEY(username) REFERENCES USER(username)
);


create table buyer(
username varchar(15),
phone varchar(15),
state varchar(15),
address varchar(30),
street varchar(15),
zip varchar(5),
city varchar(15),
PRIMARY KEY(username),
FOREIGN KEY(username) REFERENCES USER(username)
);
	

create table system_info(
user_type varchar(10),
code varchar(9)
);


create table store(
store_name varchar(30),
address varchar(30),
PRIMARY KEY(address)
);

create table payments(
username varchar(15),
default_payment boolean,
payment_name varchar(15),
acct_number char(9),
routing_number char(9)
);

create table items(
item_name varchar(15), 
description varchar(50),
exp_date varchar(10),
price varchar(5),
num_in_stock varchar(3),
category varchar(10),

PRIMARY KEY(item_name)
);

create table cart(
item_name varchar(15),
price varchar(5),
number varchar(3),

PRIMARY KEY(item_name)
);