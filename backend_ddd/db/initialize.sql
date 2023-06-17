drop table if exists transactions CASCADE;
drop table if exists wallets CASCADE;
drop type if exists transaction_mode_enum;
drop type if exists transaction_type_enum;
drop type if exists transaction_status_enum;

create type  transaction_mode_enum as enum ('QR', 'RFID', 'NFC', 'BARCODE', 'APP_TRANSFER');
create type transaction_type_enum as enum ('POS', 'P2P_PUSH', 'P2P_PULL', 'VOUCHER', 'VIRTUAL_POS', 'PAYMENT_GATEWAY', 'CARD_PAY');
create type transaction_status_enum as enum ('PENDING', 'FAILED', 'SUCCESSFUL', 'EXPIRED', 'DECLINED');

create table wallets (
    id uuid primary key,
    balance integer not null constraint  non_negative_integer check (balance >= 0),
    created_at timestamp not null default current_timestamp
);

create table transactions (
    id uuid primary key,
    amount integer not null  constraint  non_negative_integer check (amount >= 0),
    mode transaction_mode_enum not null,
    transaction_type transaction_type_enum not null,
    status transaction_status_enum not null,
    sender_wallet_id uuid References wallets(id) not null,
    recipient_wallet_id uuid References wallets(id) not null,
    created_at timestamp not null default current_timestamp,
    last_updated timestamp not null default current_timestamp
);

