create type  event_type_enum as enum ('INTERNAL', 'EXTERNAL');

alter table events
add column event_type event_type_enum;
