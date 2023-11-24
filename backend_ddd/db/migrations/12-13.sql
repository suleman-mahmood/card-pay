alter table registrations
add column tx_id uuid references transactions(id);
