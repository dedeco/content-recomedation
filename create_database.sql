CREATE DATABASE recodb;
grant usage on *.* to recouser@localhost identified by 'recopass';
grant all privileges on recodb.* to recouser@localhost ;
