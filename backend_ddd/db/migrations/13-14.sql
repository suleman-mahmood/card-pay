create table vouchers (
    code varchar,
    redeemed integer
);

-- for 50% off team

insert into vouchers (code, redeemed)
values ('XBAF', 0);

-- for 100% off team

insert into vouchers (code, redeemed)
values ('DD5N', 0);

-- for 100% off full

insert into vouchers (code, redeemed)
values ('QYNE', 0);

update registrations
set tx_id = transactions.id
from transactions
where registrations.paypro_id = transactions.paypro_id;