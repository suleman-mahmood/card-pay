----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Insert the initial version number
insert into
    version_history (id, latest_version, force_update_version)
values
    (gen_random_uuid(), '1.2.26', '1.2.22');

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Seeding CardPay wallet and user
-- Adding a random wallet
insert into wallets(id, balance, qr_id)
values (gen_random_uuid(), 1000000000, gen_random_uuid());

-- Setting a CardPay wallet
insert into starred_wallet_id
values ('297ca73c-f491-4d37-be47-60dcc36a87d7');

insert  into users (id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp)
values  ('297ca73c-f491-4d37-be47-60dcc36a87d7', 'admin@cardpay.com.pk', '+923333333333', 'CARDPAY', '2525', 'CardPay Admin', '297ca73c-f491-4d37-be47-60dcc36a87d7', true, true, 0000);

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Seeding PG wallet and user
-- Adding a random wallet
insert into wallets(id, balance, qr_id)
values (gen_random_uuid(), 0, gen_random_uuid());

insert  into users (id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp)
values  ('93c74873-294f-4d64-a7cc-2435032e3553', 'paypro@cardpay.com.pk', '+924444444444', 'PAYMENT_GATEWAY', '3434', 'PayPro Payment Gateway', '93c74873-294f-4d64-a7cc-2435032e3553', true, true, 0000);

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Give PayPro 1 million from CardPay
insert into transactions (id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id)
values (gen_random_uuid(), 1000000, 'APP_TRANSFER', 'CARD_PAY', 'SUCCESSFUL', '297ca73c-f491-4d37-be47-60dcc36a87d7', '93c74873-294f-4d64-a7cc-2435032e3553');

update wallets
set balance = 1000000
where id = '93c74873-294f-4d64-a7cc-2435032e3553';

update wallets
set balance = 999000000
where id = '297ca73c-f491-4d37-be47-60dcc36a87d7';

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Terminate db locks

SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'cardpay-prod'
  AND pid <> pg_backend_pid();

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Insert the version number
insert into
    version_history (id, latest_version, force_update_version)
values
    (gen_random_uuid(), '1.2.24', '1.2.22');

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Recent deposit requests
select
    tx.id,
    tx.created_at at time zone '+5',
    tx.last_updated at time zone '+5',
    amount,
    r.full_name as recipient_name,
    s.full_name as sender_name,
    status,
    s.loyalty_points as sender_points,
    r.loyalty_points as recipient_points
from
    transactions tx
    inner join users r on tx.recipient_wallet_id = r.wallet_id
    inner join users s on tx.sender_wallet_id = s.wallet_id
where transaction_type='PAYMENT_GATEWAY'
order by tx.created_at desc;

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Recent deposit requests for a particular user name
select
    tx.id,
    amount,
    r.full_name as recipient_name,
    s.full_name as sender_name,
    status,
    s.loyalty_points as sender_points,
    r.loyalty_points as recipient_points,
    tx.created_at
from
    transactions tx
    inner join users r on tx.recipient_wallet_id = r.wallet_id
    inner join users s on tx.sender_wallet_id = s.wallet_id
where r.full_name ilike '%Haris%' or s.full_name ilike '%Haris%'
order by tx.created_at desc;

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Information for a particular user name
select *
from users
where full_name ilike '%Mazhar%';

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Get all users who have used referral roll number
select *
from users
where referral_id != '00000000-0000-0000-0000-000000000000';

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Get all transactions of a user
select
    txn.id,
    txn.amount,
    txn.mode,
    txn.transaction_type,
    txn.status,
    txn.created_at,
    txn.last_updated,
    txn.sender_wallet_id as sender_id,
    txn.recipient_wallet_id as recipient_id,
    sender.full_name as sender_name,
    recipient.full_name as recipient_name
from
    transactions txn
    inner join users sender on txn.sender_wallet_id = sender.id
    inner join users recipient on txn.recipient_wallet_id = recipient.id
where
    (
        txn.sender_wallet_id in (
            select id from users where users.full_name ilike '%Mazhar%'
        )
        or txn.recipient_wallet_id in (
            select id from users where users.full_name ilike '%Mazhar%'
        )
    )
    and txn.status = 'SUCCESSFUL'::transaction_status_enum
order by
    txn.created_at desc;

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- For Old tables
-- Daily transactions
SELECT DATE(created_at) AS day,
       COUNT(*) AS transaction_count,
       SUM(amount) AS total_amount
FROM transactions_firestore
GROUP BY day
ORDER BY day;

-- Monthly transactions
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions_firestore
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;

-- Monthly transactions grouped by top selected vendors
with vendors as (
    select id as vendor_id, full_name as vendor_name
    from users_firestore
    where
        user_type = 'VENDOR'
        and full_name in (
            'Baradari', 'JJ Kitchen', 'JJ kitchen Main Counter', 'The Bunker'
        )
)
SELECT
    DATE_TRUNC('month', created_at) AS month,
    vendors.vendor_name AS vendor_name,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM
    transactions_firestore tx
    join vendors on vendor_id = tx.recipient_wallet_id
where tx.recipient_wallet_id in (select vendor_id from vendors)
GROUP BY DATE_TRUNC('month', created_at), vendors.vendor_name
ORDER BY month;

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Daily transactions
SELECT DATE(created_at) AS day,
       COUNT(*) AS transaction_count,
       SUM(amount) AS total_amount
FROM transactions
where
    status = 'SUCCESSFUL'

GROUP BY day
ORDER BY day desc;

-- Monthly transactions
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions
where status = 'SUCCESSFUL'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;

-- Monthly transactions grouped by top selected vendors
with vendors as (
    select id as vendor_id, full_name as vendor_name
    from users_firestore
    where
        user_type = 'VENDOR'
        and full_name in (
            'Baradari', 'JJ Kitchen', 'JJ kitchen Main Counter', 'The Bunker'
        )
)
SELECT
    DATE_TRUNC('month', created_at) AS month,
    vendors.vendor_name AS vendor_name,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM
    transactions_firestore tx
    join vendors on vendor_id = tx.recipient_wallet_id
where tx.recipient_wallet_id in (select vendor_id from vendors)
GROUP BY DATE_TRUNC('month', created_at), vendors.vendor_name
ORDER BY month;

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Find closed loop otp of a user
select *
from user_closed_loops
where user_id in (
    select id
    from users
    where full_name ilike '%Abdullah Chaud%'
);

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Daily queries!
-- Daily users that tried to sign up
select
    date(w.created_at at time zone '+5') as day,
    count(*) as user_count
from
    wallets w
group by day
order by day desc;

-- Daily users that verified their phone otp
select
    date(w.created_at at time zone '+5') as day,
    count(*) as user_count
from
    wallets w
    join users u on w.id = u.wallet_id
where
    is_phone_number_verified
group by day
order by day desc;

-- Daily users that failed to verify their phone otp
select
    date(w.created_at at time zone '+5') as day,
    count(*) as user_count
from
    wallets w
    join users u on w.id = u.wallet_id
where
    not is_phone_number_verified
group by day
order by day desc;

-- Daily users that tried to register to a closed loop
select
    date(w.created_at at time zone '+5') as day,
    count(*) as user_count
from
    wallets w
    join user_closed_loops ucl on w.id = ucl.user_id
group by day
order by day desc;

-- Daily users that verified their closed loop
select
    date(w.created_at at time zone '+5') as day,
    count(*) as user_count
from
    wallets w
    join user_closed_loops ucl on w.id = ucl.user_id
where
    ucl.status = 'VERIFIED'
group by day
order by day desc;

-- Daily users that failed to verify their closed loop
select
    date(w.created_at at time zone '+5') as day,
    count(*) as user_count
from
    wallets w
    join user_closed_loops ucl on w.id = ucl.user_id
where
    ucl.status = 'UN_VERIFIED'
group by day
order by day desc;

-- Daily users that are at the dashboard
select
    date(w.created_at at time zone '+5') as day,
    count(*) as user_count
from
    wallets w
    join users u on w.id = u.wallet_id
where
    pin != '0000'
group by day
order by day desc;

-- Daily users that have done at least one successful deposit!
with wallets_with_transactions as (
    select
        w.id as wallet_id,
        count(*),
        w.created_at
    from
        wallets w
        join transactions tx on tx.recipient_wallet_id = w.id
    where
        tx.transaction_type = 'PAYMENT_GATEWAY'
        and tx.status = 'SUCCESSFUL'
    group by w.id
)
select
    date(w.created_at at time zone '+5') as day,
    count(*) as user_count
from
    wallets w
    join wallets_with_transactions wth on wth.wallet_id = w.id
group by day
order by day desc
;

-- Daily users that have done at least one pending deposit!
with wallets_with_transactions as (
    select
        w.id as wallet_id,
        count(*),
        w.created_at
    from
        wallets w
        join transactions tx on tx.recipient_wallet_id = w.id
    where
        tx.transaction_type = 'PAYMENT_GATEWAY'
        and tx.status = 'PENDING'
    group by w.id
)
select
    date(w.created_at at time zone '+5') as day,
    count(*) as user_count
from
    wallets w
    join wallets_with_transactions wth on wth.wallet_id = w.id
group by day
order by day desc
;

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Daily checkpoints
with total_users as (
    -- Daily users that tried to sign up
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
    group by day
    order by day desc
), phone_verified_users as (
    -- Daily users that verified their phone otp
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
        join users u on w.id = u.wallet_id
    where
        is_phone_number_verified
    group by day
    order by day desc
), phone_unverified_users as (
    -- Daily users that failed to verify their phone otp
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
        join users u on w.id = u.wallet_id
    where
        not is_phone_number_verified
    group by day
    order by day desc
), lums_registered_users as (
    -- Daily users that tried to register to a closed loop
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
        join user_closed_loops ucl on w.id = ucl.user_id
    group by day
    order by day desc
), lums_verified_users as (
    -- Daily users that verified their closed loop
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
        join user_closed_loops ucl on w.id = ucl.user_id
    where
        ucl.status = 'VERIFIED'
    group by day
    order by day desc
), lums_unverified_users as (
    -- Daily users that failed to verify their closed loop
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
        join user_closed_loops ucl on w.id = ucl.user_id
    where
        ucl.status = 'UN_VERIFIED'
    group by day
    order by day desc
), signup_success_users as (
    -- Daily users that are at the dashboard
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
        join users u on w.id = u.wallet_id
    where
        pin != '0000'
    group by day
    order by day desc
),  pin_not_setup_users as (
    -- Daily users that are at the dashboard
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
        join users u on w.id = u.wallet_id
    where
        pin = '0000'
    group by day
    order by day desc
), successful_deposit_users as (
    -- Daily users that have done at least one successful deposit!
    with wallets_with_transactions as (
        select
            w.id as wallet_id,
            count(*),
            w.created_at
        from
            wallets w
            join transactions tx on tx.recipient_wallet_id = w.id
        where
            tx.transaction_type = 'PAYMENT_GATEWAY'
            and tx.status = 'SUCCESSFUL'
        group by w.id
    )
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
        join wallets_with_transactions wth on wth.wallet_id = w.id
    group by day
    order by day desc
), pending_deposit_users as (
    -- Daily users that have done at least one pending deposit!
    with wallets_with_transactions as (
        select
            w.id as wallet_id,
            count(*),
            w.created_at
        from
            wallets w
            join transactions tx on tx.recipient_wallet_id = w.id
        where
            tx.transaction_type = 'PAYMENT_GATEWAY'
            and tx.status = 'PENDING'
        group by w.id
    )
    select
        date(w.created_at at time zone '+5') as day,
        count(*) as user_count
    from
        wallets w
        join wallets_with_transactions wth on wth.wallet_id = w.id
    group by day
    order by day desc
)
select
    tu.day,
    tu.user_count as total_users,
    pvu.user_count as phone_verified_users,
    lru.user_count as lums_registered_users,
    lvu.user_count as lums_verified_users,
    ssu.user_count as signup_success_users,
    pdu.user_count as pending_deposit_users,
    sdu.user_count as successful_deposit_users,
    ((sdu.user_count * 100) / tu.user_count) as percentage_acquisition
from
    total_users tu
    join phone_verified_users pvu on pvu.day = tu.day
    join lums_registered_users lru on lru.day = tu.day
    join lums_verified_users lvu on lvu.day = tu.day
    join signup_success_users ssu on ssu.day = tu.day
    join pending_deposit_users pdu on pdu.day = tu.day
    join successful_deposit_users sdu on sdu.day = tu.day
;

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----

-- Check remaining balance in PayPro wallet
select
    balance
from
    wallets w
    join users u on w.id = u.wallet_id
where
    u.user_type = 'PAYMENT_GATEWAY'
;

-- Total users
select
    count(*) as user_count
from
    users
;

-- Total dashboard users
select
    count(*) as user_count
from
    users
where
    pin != '0000'
;

-- Users with at least one successful deposit
select
    json_agg(distinct u.full_name) as heros,
    sum(tx.amount) as total_amount,
    avg(tx.amount) as avg_amount,
    count(*) as deposit_count
from
    wallets w
    join transactions tx on tx.recipient_wallet_id = w.id
    join users u on w.id = u.wallet_id
where
    tx.transaction_type = 'PAYMENT_GATEWAY'
    and tx.status = 'SUCCESSFUL'
group by w.id
order by deposit_count desc
;

-- Frequency of deposits and their stats
with something as (
    select
        json_agg(distinct u.full_name) as heros,
        sum(tx.amount) as total_amount,
        avg(tx.amount) as avg_amount,
        count(*) as deposit_count
    from
        wallets w
        join transactions tx on tx.recipient_wallet_id = w.id
        join users u on w.id = u.wallet_id
    where
        tx.transaction_type = 'PAYMENT_GATEWAY'
        and tx.status = 'SUCCESSFUL'
    group by w.id
    order by deposit_count desc
)
select
    count(*) as no_of_users,
    deposit_count as deposit_frequency,
    sum(total_amount) as total_amount,
    avg(total_amount)::int as avg_amount
from
    something
group by deposit_count
order by no_of_users desc
;

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Daily successful deposits
select
    date(tx.created_at at time zone '+5') as day,
    count(*) as successful_deposit_count,
    sum(tx.amount) as total_amount,
    avg(tx.amount)::int as avg_amount,
    json_agg(u.full_name) as heros
from
    transactions tx
    join users u on u.id = tx.recipient_wallet_id
where
    transaction_type = 'PAYMENT_GATEWAY'
    and status = 'SUCCESSFUL'
group by day
order by day desc;

-- Daily pending deposits
select
    date(tx.created_at) as day,
    count(*) as pending_deposit_count,
    sum(tx.amount) as total_amount,
    avg(tx.amount)::int as avg_amount,
    json_agg(u.full_name) as pending_heros
from
    transactions tx
    join users u on u.id = tx.recipient_wallet_id
where
    transaction_type = 'PAYMENT_GATEWAY'
    and status = 'PENDING'
group by day
order by day desc;


----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----
-- Misc
select *
from users where phone_number = '+923333462677';

select *
from transactions tx
where tx.status = 'SUCCESSFUL'::transaction_status_enum;

select count(*)
from users u;

select REPLACE(SUBSTRING(phone_number, 4, 11), '+92', '') AS formatted_phone_number, full_name, personal_email
from users
where user_type='VENDOR';

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----

select
    *
from
    users
where
    id in (
        select user_id
        from user_closed_loops
        where users.full_name ilike '%ushb%'
    );


select * from users where full_name ilike '%saood%';
select * from user_closed_loops where user_id = 'fd0dd1db-27fa-5239-ab5a-1c22aef5ebc0';

-- The boi's (Shaheer Majid) EasyPaisa payment that didnt triggered our callback API
select
    *
from
    transactions
where
    recipient_wallet_id = 'b59619d7-4bd1-5efd-992a-fe0b390f304b'
    or sender_wallet_id = 'b59619d7-4bd1-5efd-992a-fe0b390f304b'
;

with boi_id as (
    select
        id
    from users_firestore
    where personal_email = '24040064@lums.edu.pk'
)
select
    amount,
    created_at
from
    transactions_firestore
where
    sender_wallet_id in (select id from boi_id);

with boi_id as (
    select
        id
    from users_firestore
    where personal_email = '24040064@lums.edu.pk'
)
select
    amount,
    created_at
from
    transactions_firestore
where
    recipient_wallet_id in (select id from boi_id)
;

select avg(amount)
from transactions
where
    recipient_wallet_id in (
        select  id
        from users
        where
            full_name ilike '%Khokha%'
            and user_type = 'VENDOR'
    )
    and amount > 20
    and status = 'SUCCESSFUL'
;

select *
from wallets
where id in (
    select id
    from users
    where user_type='PAYMENT_GATEWAY'
    )
;

-- Get vendor transactions before a reconcile
select
    sum(amount),
    s.full_name
from
    transactions tx
    inner join users r on tx.recipient_wallet_id = r.wallet_id
    inner join users s on tx.sender_wallet_id = s.wallet_id
where
    r.user_type = 'CARDPAY'
    and s.user_type = 'VENDOR'
    and tx.created_at > current_date - interval '3 hour'
group by s.full_name
;

select
    *
from transactions
where
    recipient_wallet_id in (
            select id from users where phone_number = '+923001827102'
        )
    and transaction_type = 'PAYMENT_GATEWAY'
;

-- Get signups for all ambassador
select
    *
from
    users u
    join users r on r.id = u.referral_id
;

SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount)::INT AS avg_amount
FROM
    transactions
where
    status = 'SUCCESSFUL'
    and transaction_type != 'CARD_PAY'

GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;

----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----

-- Search user from full name
select
    *
from
    users
    join wallets w on users.wallet_id = w.id
--     join user_closed_loops ucl on users.id = ucl.user_id
where
    full_name ilike '%Reem%'
;

-- Search user from phone number
select * from users where phone_number ilike '%3214414839%';

-- Search roll number using phone number
select
    *
from user_closed_loops
where
    user_id in (
            select id from users where phone_number like '+%3227139653%'
        )
;
-- Search user from unique identifier
select
    *
from
    user_closed_loops
--     join users u on u.id = user_closed_loops.user_id
where
    unique_identifier ilike '%207%'
;

-- Search user using roll number
select
    *
from
    users
where id in (
    select
        user_id
    from
        user_closed_loops
    where unique_identifier ilike '%27100131%'
    )
;

-- Search transaction from id
select
    *
from
    transactions
where
    id = '0b069401-915d-4197-80fd-feaaa6e38d96'
;
----- ----- ----- ----- -----  ----- ----- ----- ----- -----  ----- ----- ----- ----- ----- ----- ----- ----- -----

-- Last 5 users
select * from users order by created_at desc limit 5;

-- Drop areej rows
select * from users where id = 'c568929a-f0d1-522d-8365-f3be2d7b1210';
select * from user_closed_loops where user_id = 'c568929a-f0d1-522d-8365-f3be2d7b1210';
select * from wallets where id = 'c568929a-f0d1-522d-8365-f3be2d7b1210';
select * from transactions where recipient_wallet_id = 'c568929a-f0d1-522d-8365-f3be2d7b1210';
select * from transactions where sender_wallet_id = 'c568929a-f0d1-522d-8365-f3be2d7b1210';

select * from events;


-- Users who made a pending deposit but never a successful deposit
with successful_deposits as (
    select w.id
    from wallets w
        join transactions tx on tx.recipient_wallet_id = w.id
        join users u on w.id = u.wallet_id
    where
        tx.transaction_type = 'PAYMENT_GATEWAY'
        and tx.status = 'SUCCESSFUL'
    group by w.id
), pending_deposits as (
    select w.id
    from wallets w
        join transactions tx on tx.recipient_wallet_id = w.id
        join users u on w.id = u.wallet_id
    where
        tx.transaction_type = 'PAYMENT_GATEWAY'
        and tx.status = 'PENDING'
    group by w.id
)
select
    *
from
    users u
    left join successful_deposits sd on u.id = sd.id
    inner join pending_deposits pd on pd.id = u.id
where
    sd.id is null
;

-- Average transaction amount for a vendor
select
    avg(amount)
from
    transactions tx
    join users u on u.id = tx.recipient_wallet_id
where
    u.user_type = 'VENDOR'
    and u.full_name ilike '%Khokha%'
;

select
    *
from
    transactions
where
    status = 'SUCCESSFUL'
    and transaction_type = 'PAYMENT_GATEWAY'
    and last_updated >  '2023-10-01'
;

select
    json_agg(distinct u.full_name) as heros,
    sum(tx.amount) as total_amount,
    avg(tx.amount) as avg_amount,
    count(*) as deposit_count
from
    wallets w
    join transactions tx on tx.recipient_wallet_id = w.id
    join users u on w.id = u.wallet_id
where
    tx.transaction_type = 'PAYMENT_GATEWAY'
    and tx.status = 'PENDING'
group by w.id
order by deposit_count desc
;

--
select * from users where full_name ilike '%Sul%'

select
    id,
    amount,
    mode,
    transaction_type,
    status,
    sender_wallet_id,
    recipient_wallet_id,
    created_at,
    last_updated
from
    transactions
where
    recipient_wallet_id = '70402d77-6e1c-57e9-8df0-ee0698db7047'
    and transaction_type = 'PAYMENT_GATEWAY'::transaction_type_enum
order by
    created_at desc
limit 1
;