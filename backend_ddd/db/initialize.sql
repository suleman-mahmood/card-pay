drop table if exists transactions CASCADE;
drop table if exists wallets CASCADE;
drop table if exists closed_loops CASCADE;
drop table if exists users CASCADE;
drop table if exists user_closed_loops CASCADE;
drop type if exists transaction_mode_enum CASCADE;
drop type if exists transaction_type_enum CASCADE;
drop type if exists transaction_status_enum CASCADE;
drop type if exists closed_loop_verification_type CASCADE;
drop type if exists user_type_enum CASCADE;
drop type if exists closed_loop_user_state_enum CASCADE;

create type  transaction_mode_enum as enum ('QR', 'RFID', 'NFC', 'BARCODE', 'APP_TRANSFER');
create type transaction_type_enum as enum ('POS', 'P2P_PUSH', 'P2P_PULL', 'VOUCHER', 'VIRTUAL_POS', 'PAYMENT_GATEWAY', 'CARD_PAY');
create type transaction_status_enum as enum ('PENDING', 'FAILED', 'SUCCESSFUL', 'EXPIRED', 'DECLINED');
create type closed_loop_verification_type as enum ('NONE','ROLLNUMBER','EMAIL','MEMBERSHIP_ID');
create type user_type_enum as enum ('CUSTOMER','VENDOR','ADMIN','PAYMENT_GATEWAY','CARDPAY');
create type closed_loop_user_state_enum as enum ('UN_VERIFIED','VERIFIED');

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

create table closed_loops(
    id uuid primary key,
    name varchar(255) not null,
    logo_url varchar(255) not null,
    description varchar(255) not null,
    regex varchar(255) not null,
    verification_type closed_loop_verification_type not null,
    created_at timestamp not null default current_timestamp
);

create table users (
    id uuid primary key,
    personal_email varchar(255) not null,
    phone_number varchar(255) not null,
    user_type user_type_enum not null,
    pin varchar(4) not null,
    full_name varchar(255) not null,
    wallet_id uuid References wallets(id) not null,
    is_active boolean not null,
    is_phone_number_verified boolean not null,
  
    otp varchar(4) not null,
    otp_generated_at timestamp not null default current_timestamp,
    location point not null default point(0,0),
    created_at timestamp not null default current_timestamp
    


);

create table user_closed_loops (
    
    user_id uuid references users(id),
    closed_loop_id uuid references closed_loops(id),

    unique_identifier varchar(255) not null,
    closed_loop_user_id varchar(255) not null,
    unique_identifier_otp varchar(4) not null,
    status closed_loop_user_state_enum not null,
    created_at timestamp not null default current_timestamp,

    primary key (user_id, closed_loop_id)
);
