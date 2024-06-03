create database event_management_system;
use event_management_system;
create table event_host(
event_host_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null unique,
phone varchar(255) not null unique,
password varchar(255) not null,
address varchar(255) not null,
status varchar(255) not null,
profile_pic varchar(255) not null
);
create table event_type(
event_type_id int auto_increment primary key,
event_type varchar(255) not null ,
event_type_pic varchar(255) not null
);
create table places(
places_id int auto_increment primary key,
name varchar(255) not null,
address varchar(255) not null
);
create table customer(
customer_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null unique,
phone varchar(255) not null unique,
password varchar(255) not null,
gender varchar(255) not null,
profile_pic varchar(255) not null
);
create table coupons(
coupons_id int auto_increment primary key,
coupon_name varchar(255) not null,
description varchar(255) not null,
validity_upto varchar(255) not null,
discount int not null,
status varchar(255) not null,
event_host_id int not null,
foreign key(event_host_id) references event_host(event_host_id)
);
create table event(
event_id int auto_increment primary key,
event_pic varchar(255) not null,
event_title varchar(255) not null,
event_date date not null,
start_date_time datetime not null,
end_date_time datetime not null,
description varchar(255) not null,
cost_per_person varchar(255) not null,
event_host_id int not null,
event_type_id int not null,
places_id int not null,
layout varchar(255) not null,
number_of_tickets int not null,
foreign key(event_host_id) references event_host(event_host_id),
foreign key(event_type_id) references event_type(event_type_id),
foreign key(places_id) references places(places_id)
);
create table booking(
booking_id int auto_increment primary key,
number_of_tickets int not null,
ticket_price int not null,
tax int not null,
convenience_fee int not null,
donations int ,
total_amount int not null,
date datetime default current_timestamp,
status varchar(255) not null,
event_id int not null,
coupons_id int ,
customer_id int not null,
foreign key(event_id) references event(event_id),
foreign key(coupons_id) references coupons(coupons_id),
foreign key(customer_id) references customer(customer_id)
);
create table payment(
payment_id int auto_increment primary key,
card_holder_name varchar(255) not null,
card_number varchar(255) not null,
cvv varchar(255) not null,
expiry_date varchar(255) not null,
amount float not null,
date datetime default current_timestamp,
status varchar(255) not null,
booking_id int not null,
foreign key(booking_id) references booking(booking_id)
);
create table review_rating(
review_rating_id int auto_increment primary key,
review varchar(255) not null,
rating int not null,
date datetime default current_timestamp,
booking_id int not null,
foreign key(booking_id) references booking(booking_id)
);
create table booked_seats(
booked_seats_id int auto_increment primary key,
booking_id int not null,
seat_numbers varchar(255) not null,
status varchar(255) not null,
foreign key(booking_id) references booking(booking_id)
);