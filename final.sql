create table applicant
(
    applicant_id    varchar(20) primary key,
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
    resume_id       varchar(20) primary key,
    file_name       varchar(20),
    file_path       varchar(20)
)ENGINE=INNODB;

create table company
(
    company_id          varchar(20) primary key,
    company_name        varchar(20),
    address             varchar(20),
    phone               varchar(20),
    website             varchar(20),
    category            varchar(20)
) ENGINE=INNODB;

create table job
(
    job_id              varchar(20) primary key,
    job_name            varchar(20),
    company_id          varchar(20),
    requirement         varchar(20),
    category            varchar(20),
    description         varchar(100),
    foreign key ( company_id) references company( company_id)
) ENGINE=INNODB;

create table events
(
    event_id        varchar(20) primary key,
    event_name      varchar(20),
    website         varchar(20),
    category        varchar(20),
    description     varchar(20),
    start_time      DATETIME,
    end_time        DATETIME
)ENGINE=INNODB;

create table admin
(
    admin_id        varchar(20) primary key,
    password        varchar(20),
    name            varchar(20),
    hash_value      varchar(20),
    uu_id           varchar(20)

)ENGINE=INNODB;

create table employs
(
    applicant_id    varchar(20) primary key,
    company_id      varchar(20) 
)ENGINE=INNODB;

create table apply
(
    applicant_id    varchar(20) primary key,
    job_id      varchar(20),
    data        DATETIME,
    resume_id   varchar(20),
    state       varchar(20),
    foreign key (applicant_id) references applicant(applicant_id),
    foreign key (job_id) references job(job_id),
    foreign key (resume_id) references resume(resume_id)
)ENGINE=INNODB;

create table participate
(
    event_id    varchar(20) primary key,
    applicant_id   varchar(20)
)ENGINE=INNODB;

create table submit
(
    job_id  varchar(20) primary key,
    resume_id varchar(20),
    foreign key (job_id) references job(job_id)
)ENGINE=INNODB;

create table sponse
(
    event_id  varchar(20) primary key,
    company_id  varchar(20)
)ENGINE=INNODB;
