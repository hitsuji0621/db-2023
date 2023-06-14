drop database team7;
create database team7;
use team7;
create table applicant
(
    applicant_id    int primary key AUTO_INCREMENT,
    email           varchar(20),
    password        varchar(20),
    zh_name         varchar(20),
    phone           varchar(20),
    gender          varchar(20),
    birthday        DATE,
    update_time     DATETIME,
    picture         varchar(20)
)ENGINE=INNODB;

create table resume
(
    resume_id       int primary key AUTO_INCREMENT,
    resume_url      varchar(200)
)ENGINE=INNODB;

create table company
(
    company_id          int primary key AUTO_INCREMENT,
    company_name        varchar(20),
    address             varchar(20),
    phone               varchar(20),
    website             varchar(20),
    category            varchar(20),
    password            varchar(20)
) ENGINE=INNODB;

create table job
(
    job_id              int primary key AUTO_INCREMENT,
    job_name            varchar(20),
    company_id          int,
    requirement         varchar(100),
    category            varchar(20),
    description         varchar(100),
    foreign key ( company_id) references company( company_id)
) ENGINE=INNODB;

create table events
(
    event_id        int primary key AUTO_INCREMENT,
    event_name      varchar(20),
    website         varchar(20),
    category        varchar(20),
    description     varchar(20),
    start_time      DATETIME,
    end_time        DATETIME
)ENGINE=INNODB;

create table admin
(
    admin_id        int primary key AUTO_INCREMENT,
    password        varchar(20),
    name            varchar(20),
    hash_value      varchar(20),
    uu_id           int
)ENGINE=INNODB;

create table employs
(
    applicant_id    int ,
    company_id      int,
    primary key(applicant_id,company_id)
)ENGINE=INNODB;

create table apply
(
    applicant_id    int ,
    job_id      int ,
    date        DATETIME,
    resume_id   int,
    state       varchar(20),
    primary key(applicant_id,job_id),
    foreign key (applicant_id) references applicant(applicant_id),
    foreign key (job_id) references job(job_id),
    foreign key (resume_id) references resume(resume_id)
)ENGINE=INNODB;

create table participate
(
    event_id    int,
    applicant_id   int,
    primary key(event_id,applicant_id)
)ENGINE=INNODB;

create table sponse
(
    event_id  int,
    company_id  int,
    primary key(event_id,company_id)
)ENGINE=INNODB;

