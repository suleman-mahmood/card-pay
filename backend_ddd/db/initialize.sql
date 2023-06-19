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

create closed_loops(
    id uuid primary key,
    name varchar(255) not null,
    logo_url varchar(255) not null,
    description varchar(255) not null,
    regex varchar(255) not null,
    verification_type varchar(255) not null,
    created_at timestamp not null
)

create table users (
    id uuid primary key,
    personal_email varchar(255) not null,
    phone_number varchar(255) not null,
    user_type varchar(255) not null,
    pin varchar(255) not null,
    full_name varchar(255) not null,
    wallet_id uuid References wallets(id) not null,
    is_active boolean not null,
    is_phone_number_verified boolean not null,
  
    otp varchar(255) not null,
    otp_generated_at timestamp not null,
    location point not null,
    created_at timestamp not null,
    


);

create table user_closed_loops (
    
    user_id uuid references users(id),
    closed_loop_id uuid references closed_loops(id),
    
    unique_indentifier varchar(255) not null,
    closed_loop_user_id varchar(255) not null,
    unique_indentifier_otp varchar(255) not null,
    status varchar(255) not null,
    created_at timestamp not null,

    primary key (user_id, closed_loop_id)
)
