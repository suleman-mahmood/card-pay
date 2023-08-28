drop table if exists transactions cascade;
drop table if exists wallets cascade;
drop table if exists closed_loops cascade;
drop table if exists users cascade;
drop table if exists user_closed_loops cascade;
drop table if exists weightages cascade;
drop table if exists cashback_slabs cascade;
drop table if exists starred_wallet_id cascade;
drop table if exists payment_gateway_tokens cascade;
drop table if exists wallets_firestore cascade;
drop table if exists users_firestore cascade;
drop table if exists transactions_firestore cascade;

drop type if exists transaction_mode_enum cascade;
drop type if exists transaction_type_enum cascade;
drop type if exists transaction_status_enum cascade;
drop type if exists closed_loop_verification_type cascade;
drop type if exists user_type_enum cascade;
drop type if exists closed_loop_user_state_enum cascade;
drop type if exists cashback_type_enum cascade;

create type  transaction_mode_enum as enum ('QR', 'RFID', 'NFC', 'BARCODE', 'APP_TRANSFER');
create type transaction_type_enum as enum ('POS', 'P2P_PUSH', 'P2P_PULL', 'VOUCHER', 'VIRTUAL_POS', 'PAYMENT_GATEWAY', 'CARD_PAY', 'CASH_BACK', 'REFERRAL');
create type transaction_status_enum as enum ('PENDING', 'FAILED', 'SUCCESSFUL', 'EXPIRED', 'DECLINED');
create type closed_loop_verification_type as enum ('NONE','ROLLNUMBER','EMAIL','MEMBERSHIP_ID');
create type user_type_enum as enum ('CUSTOMER','VENDOR','ADMIN','PAYMENT_GATEWAY','CARDPAY');
create type closed_loop_user_state_enum as enum ('UN_VERIFIED','VERIFIED');
create type cashback_type_enum as enum ('PERCENTAGE','ABSOLUTE');


create table wallets (
    id uuid primary key,
    balance integer not null constraint  non_negative_integer check (balance >= 0),
    created_at timestamp not null default current_timestamp
);

create table starred_wallet_id (
    wallet_id uuid references wallets(id)
);

create table transactions (
    id uuid primary key,
    amount integer not null  constraint  non_negative_integer check (amount >= 0),
    mode transaction_mode_enum not null,
    transaction_type transaction_type_enum not null,
    status transaction_status_enum not null,
    sender_wallet_id uuid references wallets(id) not null,
    recipient_wallet_id uuid references wallets(id) not null,
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
    wallet_id uuid references wallets(id) not null,
    is_active boolean not null,
    is_phone_number_verified boolean not null,
    otp varchar(4) not null,
    otp_generated_at timestamp not null default current_timestamp,
    location point not null default point(0,0),
    created_at timestamp not null default current_timestamp,
    loyalty_points integer not null default 0,
    referral_id uuid not null default '00000000-0000-0000-0000-000000000000'  
);


create table user_closed_loops (
    
    user_id uuid references users(id),
    closed_loop_id uuid references closed_loops(id),

    unique_identifier varchar(255),
    closed_loop_user_id varchar(255) not null,
    unique_identifier_otp varchar(4) not null,
    status closed_loop_user_state_enum not null,
    created_at timestamp not null default current_timestamp,
    unique (closed_loop_id, unique_identifier),
    primary key (user_id, closed_loop_id)
);

create table weightages (
    
    weightage_type transaction_type_enum primary key,
    weightage_value float not null
);

create table cashback_slabs (

    start_amount float not null,
    end_amount float not null,
    cashback_type cashback_type_enum not null,
    cashback_value float not null,
    id uuid primary key
);
  
create table payment_gateway_tokens (
    id varchar(255) primary key,
    token varchar(255) not null,
    last_updated timestamp not null default current_timestamp
);


-- Migration content

create table wallets_firestore (
    id uuid primary key,
    balance integer not null constraint  non_negative_integer check (balance >= 0),
    created_at timestamp not null default current_timestamp,

    migrated boolean not null default false -- The only difference here
);

create table users_firestore (
    id uuid primary key,
    personal_email varchar(255) not null,
    phone_number varchar(255) not null,
    user_type user_type_enum not null,
    pin varchar(4) not null,
    full_name varchar(255) not null,
    wallet_id uuid references wallets_firestore(id) not null, -- fk
    is_active boolean not null,
    is_phone_number_verified boolean not null,
    otp varchar(4) not null,
    otp_generated_at timestamp not null default current_timestamp,
    location point not null default point(0,0),
    created_at timestamp not null default current_timestamp,
    loyalty_points integer not null default 0,
    referral_id uuid not null default '00000000-0000-0000-0000-000000000000',

    migrated boolean not null default false -- The only difference here
);

create table transactions_firestore (
    id uuid primary key,
    amount integer not null  constraint  non_negative_integer check (amount >= 0),
    mode transaction_mode_enum not null,
    transaction_type transaction_type_enum not null,
    status transaction_status_enum not null,
    sender_wallet_id uuid references wallets_firestore(id) not null, -- fk
    recipient_wallet_id uuid references wallets_firestore(id) not null, -- fk
    created_at timestamp not null default current_timestamp,
    last_updated timestamp not null default current_timestamp,

    migrated boolean not null default false -- The only difference here
);
