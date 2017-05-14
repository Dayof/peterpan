drop table if exists user;
create table user (
  user_id integer not null primary key,
  id_local text not null,
  id_link text not null
);

drop table if exists local;
create table local (
  id_local integer not null primary key AUTOINCREMENT,
  local text not null,
);

drop table if exists link;
create table link (
  id_link integer not null primary key AUTOINCREMENT,
  link text not null,
  tags text,
);
