create type event_status_enum as enum ('DRAFT', 'APPROVED', 'CANCELLED');
create type event_attendance_status as enum ('UN_ATTENDED', 'ATTENDED');

create table events (
    id uuid primary key,
    status event_status_enum not null,
    cancellation_reason varchar(255),
    name varchar(255) not null,
    organizer_id uuid not null,
    venue varchar(255) not null,
    capacity int not null,
    description varchar(255) not null,
    image_url varchar(255) not null,
    closed_loop_id uuid not null,
    event_start_timestamp timestamp not null,
    event_end_timestamp timestamp not null,
    registration_start_timestamp timestamp not null,
    registration_end_timestamp timestamp not null,
    registration_fee int not null,
    created_at timestamp not null default current_timestamp
);

create table registrations (
    qr_id uuid primary key,
    user_id uuid not null,
    attendance_status event_attendance_status not null,
    event_id uuid not null references events(id),
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp
);
