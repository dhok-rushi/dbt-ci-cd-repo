{{ config(
    schema='STAGING',
    materialized='view'
) }}

select

    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    state,
    signup_date,
    customer_status,
    updated_at

from {{ source('raw', 'raw_customers') }}