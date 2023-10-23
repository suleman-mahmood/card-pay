alter table registrations
add column event_form_data jsonb;

alter table events
add column event_form_schema jsonb;