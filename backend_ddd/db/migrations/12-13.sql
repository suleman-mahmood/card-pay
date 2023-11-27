alter table registrations
add column tx_id uuid references transactions(id);
alter type transaction_status_enum add value 'TO_REVERSE';
alter type transaction_status_enum add value 'REVERSED';
alter type transaction_type_enum add value 'REVERSAL';
