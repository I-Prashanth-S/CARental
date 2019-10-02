create table customer
(
    username varchar(255),
    driving_license_no varchar(255),
    password  varchar(255),
    primary key(username)
);

create table customer_identity
(
    driving_license_no varchar(255) not null, 
    first_name varchar(255), 
    middle_name varchar(255), 
    last_name varchar(255), 
    email_id varchar(255), 
    customer_address varchar(255),
    primary key(driving_license_no)
);

create table customer_Phone
(
    driving_license_no  VARCHAR(255),
    phone_no VARCHAR(255),
    primary key(driving_license_no,phone_no)
);


create table booking
(
    username varchar(255),
    car_registration_no varchar(255),
    bill_time varchar(255),
    bill_date varchar(255),
    booking_id varchar(255),
    is_local varchar(255),
    is_insure varchar(255),
    password varchar(255),
    pickup_date varchar(255),
    return_date varchar(255),
    booking_status varchar(255),
    expected_return_date varchar(255),
    pickup_time varchar(255),
    date_of_rental varchar(255),

    primary key(booking_id)
);



create table Billing
(
    Booking_id varchar(255), 
    Total_amount varchar(255), 
    Tax varchar(255),
    Discount varchar(255), 
    Bill_status varchar(255), 
    Days_delayed varchar(255), 
    Rating varchar(255), 
    Comments varchar(255), 
    primary key(Booking_id)
);


create table Car 
(
    car_registration_no varchar(255),
    Availability_status varchar(255),   
    category varchar(255),   
    model varchar(255),   
    mileage varchar(255),   
    car_dealer_address varchar(255)
);

create table location
(
    car_dealer_address varchar(255),
    city_name varchar(255)
);

create table pricing
(
    category varchar(255),
    price varchar(255)
);