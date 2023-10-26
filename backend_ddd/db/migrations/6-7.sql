alter table events 
alter column description type text;

alter table registrations
add column paypro_id text;
