create table promotion
(
    id_promotion     INT     auto_increment
        primary key,
    promotion_name   varchar(20) null,
    p_start_date     datetime   null,
    p_end_date       datetime   null,
    percent_discount int         null
);

create table room_type
(
    name_type    varchar(10) not null
        primary key,
    price        float       not null,
    description  varchar(400) not null
);

create table apply_promotion
(
    id_promotion int     auto_increment,
    name_type    varchar(10) not null,
    description  varchar(400) not null,
    primary key (id_promotion, name_type),
    constraint FK_promotion_id
        foreign key (id_promotion) references promotion (id_promotion),
    constraint FK_promotion_name_type
        foreign key (name_type) references room_type (name_type)
);

create table room
(
    room_number char(3)     not null
        primary key,
    name_type   varchar(10) null,
    constraint FK_name_room
        foreign key (name_type) references room_type (name_type)
);

create table staff
(
    id_staff      int     AUTO_INCREMENT
        primary key,
    s_fiscal_code char(16)    unique ,
    s_password    varchar(20) not null,
    s_name        varchar(20) null,
    s_surname     varchar(20) null,
    s_email       varchar(20) unique ,
    s_gender      char        null,
    role          varchar(15) not null
);

create table cleaning
(
    cleaning_date timestamp not null,
    room_number   char(3)   not null,
    id_staff      int   not null,
    primary key (cleaning_date, room_number, id_staff),
    constraint FK_cleaning_room
        foreign key (room_number) references room (room_number),
    constraint FK_cleaning_staff_id
        foreign key (id_staff) references staff (id_staff)
);

create table news
(
    id_news           int  AUTO_INCREMENT
        primary key,
    title            varchar(20) not null,
    publication_date datetime not null,
    description      varchar(400) not null,
    id_staff          int  null,
    constraint FK_news_id_staff
        foreign key (id_staff) references staff (id_staff)
);

create table user
(
    id_user              int primary key ,
    matriculation_number char(10)    unique not null,
    email                varchar(20) unique null,
    fiscal_code          char(16)    not null,
    password             varchar(20) not null,
    name                 varchar(20) not null,
    surname              varchar(20) not null,
    gender               char(1)        null,
    role                 varchar(20) null,
    constraint fiscal_code
        unique (fiscal_code)
);

create table assistance
(
    assistance_date      datetime not null,
    feedback             int       null,
    id_staff             int   not null,
    id_user int  not null,
    primary key (assistance_date, id_staff, id_user),
    constraint FK_asst_id_staff
        foreign key (id_staff) references staff (id_staff),
    constraint FK_asst_id_user
        foreign key (id_user) references user (id_user)
);

create table reservation
(
    id_reservation       int    auto_increment
        primary key,
    check_in_date        datetime   not null,
    check_out_date       datetime   not null,
    reservation_date     datetime   not null,
    start_date           datetime   null,
    end_date             datetime   null,
    id_user              int    not null,
    name_type            varchar(10) not null,
    room_number          char(3)     not null,
    constraint FK_book_id_user
        foreign key (id_user) references user (id_user),
    constraint FK_book_name_type
        foreign key (name_type) references room_type (name_type),
    constraint FK_book_room_number
        foreign key (room_number) references room (room_number)
);

create table payment
(
    receipt_number char(6)   not null
        primary key,
    total          float     not null,
    payment_date   timestamp not null,
    id_reservation int  null,
    constraint FK_payment_id_reservation
        foreign key (id_reservation) references reservation (id_reservation)
);

create table review
(
    review_id      int      not null
        primary key,
    vote           int       not null,
    title          varchar(20) null,
    description    varchar(400) null,
    review_date    timestamp null,
    id_reservation int  null,
    constraint FK_review_id_reservation
        foreign key (id_reservation) references reservation (id_reservation)
);