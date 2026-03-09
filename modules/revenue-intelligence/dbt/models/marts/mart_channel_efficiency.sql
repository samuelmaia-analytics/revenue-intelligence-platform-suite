with customer_lifetime as (
    select * from {{ ref('int_customer_lifetime') }}
)

select
    channel,
    segment,
    avg(lifetime_revenue) as avg_ltv,
    avg(total_orders) as avg_orders_per_customer,
    count(*) as customers
from customer_lifetime
group by 1, 2
