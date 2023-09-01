# создание таблицы с данными о компаниях
CREATE TABLE companies
(
    company_id integer PRIMARY KEY NOT NULL ,
    company_name character varying(50) NOT NULL,
    description text,
    link character varying(200)
   )

# создание таблицы с данными о вакансиях
CREATE TABLE vacancies
(
vacancy_id integer NOT NULL,
company_id integer REFERENCES companies(company_id) NOT NULL,
vacancy_name character varying(100) NOT NULL,
salary integer,
link character varying(200) NOT NULL,
description text,
experience character varying(60)
)
