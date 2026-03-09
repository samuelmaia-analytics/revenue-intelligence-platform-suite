with enriched as (
    select * from {{ ref('int_orders_enriched') }}
)

select
    customer_id,
    min(signup_date) as signup_date,
    min(channel) as channel,
    min(segment) as segment,
    count(distinct order_id) as total_orders,
    sum(order_value) as lifetime_revenue,
    max(order_date) as last_order_date,
    min(order_date) as first_order_date,
    date_diff(max(order_date), min(order_date), day) as active_days
from enriched
group by customer_id
