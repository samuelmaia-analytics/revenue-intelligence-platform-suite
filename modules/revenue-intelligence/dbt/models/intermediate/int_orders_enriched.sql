with orders as (
    select * from {{ ref('stg_orders') }}
),
customers as (
    select * from {{ ref('stg_customers') }}
)

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_value,
    c.channel,
    c.segment,
    c.signup_date,
    {{ dbt.datediff('c.signup_date', 'o.order_date', 'day') }} as customer_tenure_days,
    {{ dbt.date_trunc('month', 'o.order_date') }} as order_month
from orders o
inner join customers c
    on o.customer_id = c.customer_id
