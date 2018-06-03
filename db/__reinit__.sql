drop table sessions;
drop table registrations;
drop table attempts;
drop table tasks;
drop table olymps;
drop table projects;
drop table users;

create table users (
    uid serial not null primary key,
    login varchar(50) not null,
    password varchar(50) not null
);

create table projects (
    pid serial not null primary key,
    author int not null,
    name varchar(50),
    code varchar,
    tests varchar,
    verifier varchar,
    optimization varchar(3),
    response_type int,
    foreign key (author) references users(uid)
);

create table olymps (
    oid serial not null primary key,
    author int not null,
    name varchar(50),
    start_time timestamp,
    end_time timestamp,
    foreign key (author) references users(uid)
);

create table tasks (
    tid serial not null primary key,
    oid int not null,
    name varchar(50),
    description varchar,
    pid int not null,
    foreign key (oid) references olymps(oid),
    foreign key (pid) references projects(pid)
);

create table attempts (
    aid serial not null primary key,
    tid int not null,
    uid int not null,
    result int,
    foreign key (tid) references tasks(tid),
    foreign key (uid) references users(uid)
);

create table registrations (
    uid int not null,
    oid int not null,
    primary key (uid, oid),
    foreign key (uid) references users(uid),
    foreign key (oid) references olymps(oid)
);

create table sessions (
    sid char(36) not null primary key,
    uid int not null,
    foreign key (uid) references users(uid),
    expired date
);

