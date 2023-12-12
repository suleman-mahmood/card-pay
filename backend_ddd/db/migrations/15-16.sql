alter table users
add column public_key bytea,
add column private_key bytea;

create table rp_transactions (
    tx_id uuid primary key references transactions(id) not null,
    document_id varchar
)
reate