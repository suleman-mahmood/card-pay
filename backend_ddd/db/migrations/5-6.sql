create table fcm_tokens (
    user_id uuid primary key references users(id),
    fcm_token varchar(255) not null
);