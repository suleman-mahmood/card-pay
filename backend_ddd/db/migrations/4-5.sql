ALTER TABLE registrations
ADD COLUMN event_form_data jsonb;

ALTER TABLE events
ADD COLUMN event_form_schema jsonb;