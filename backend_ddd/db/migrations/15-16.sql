alter table users
add column public_key text,
add column private_key text;

create table rp_transactions (
    tx_id uuid primary key references transactions(id) not null,
    document_id varchar
)