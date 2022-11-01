set schema
  'snomedct';

/*create table nursingactivityrefset_f*/
drop table if exists nursingactivityrefset_f cascade;

create table nursingactivityrefset_f(
	id uuid not null,
	effectivetime char(8) not null,
	active char(1) not null,
	moduleid varchar(18) not null,
	refsetid varchar(18) not null,
	referencedcomponentid varchar(18) not null,
	PRIMARY KEY(id, effectivetime)
);

/*create table nursinghealthissuesrefset_f*/
drop table if exists nursinghealthissuesrefset_f cascade;

create table nursinghealthissuesrefset_f(
  	id uuid not null,
  	effectivetime char(8) not null,
  	active char(1) not null,
  	moduleid varchar(18) not null,
  	refsetid varchar(18) not null,
  	referencedcomponentid varchar(18) not null,
  	PRIMARY KEY(id, effectivetime)
);