create table applicant
(
    applicant_id    varchar(20) primary key AUTO_INCREMENT,
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
    resume_id       varchar(20) primary key AUTO_INCREMENT,
    file_name       varchar(20),
    file_path       varchar(20)
)ENGINE=INNODB;
create table apply
(
    applylicant_id  varchar(20) primary key AUTO_INCREMENT,
    job_id          varchar(20),
    date            varchar(20),
    resume_id       varchar(20),
    state           varchar(20)
    foreign key (resume_id) references resume(resume_id)
)ENGINE=INNODB;

create table company
(
    company_id          varchar(20) primary key AUTO_INCREMENT,
    company_name        varchar(20),
    address             varchar(20),
    phone               varchar(20),
    website             varchar(20),
    category            varchar(20)
)ENGINE=INNODB;

create table job
(
    job_id              varchar(20) primary key AUTO_INCREMENT,
    job_name            varchar(20) ,
    company             varchar(20) ,
    requirement         varchar(20) ,
    category            varchar(20) ,
    description         varchar(100),
    foreign key (company) references company(company_name)
)ENGINE=INNODB;


create table events
(
    event_id        varchar(20) primary key AUTO_INCREMENT,
    event_name      varchar(20),
    website         varchar(20),
    category        varchar(20),
    description     varchar(20),
    start_time      DATETIME,
    end_time        DATETIME
)ENGINE=INNODB;

create table admin
(
    admin_id        varchar(20) primary key AUTO_INCREMENT,
    password        varchar(20),
    name            varchar(20),
    hash_value      varchar(20),
    uu_id           varchar(20)

)ENGINE=INNODB;

create table hire
(
    applicant_id    varchar(20) primary key AUTO_INCREMENT,
    company_id      varchar(20),
    foreign key (applicant_id) references applicant(applicant_id),
    foreign key (company_id) references company(company_id)
)ENGINE=INNODB;

create table apply
(
    applicant_id    varchar(20) primary key AUTO_INCREMENT,
    job_id      varchar(20),
    data        DATETIME,
    state       varchar(20),
    foreign key (applicant_id) references applicant(applicant_id),
    foreign key (job_id) references job(job_id)
)ENGINE=INNODB;

create table participate
(
    event_id    varchar(20) primary key AUTO_INCREMENT,
    applicant_id   varchar(20),
    foreign key (applicant_id) references applicant(applicant_id),
    foreign key (event_id) references events(event_id)
)ENGINE=INNODB;

create table submit
(
    job_id  varchar(20),
    resume_id varchar(20),
    foreign key (job_id) references job(job_id)
)ENGINE=INNODB;

create table sponse
(
    event_id  varchar(20),
    company_id  varchar(20)
)ENGINE=INNODB;
