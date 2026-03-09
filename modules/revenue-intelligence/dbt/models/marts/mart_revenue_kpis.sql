with orders as (
    select * from {{ ref('int_orders_enriched') }}
)

select
    order_month,
    channel,
    segment,
    sum(order_value) as revenue,
    count(distinct order_id) as orders,
    count(distinct customer_id) as active_customers,
    case
        when count(distinct order_id) = 0 then null
        else sum(order_value) / count(distinct order_id)
    end as aov
from orders
group by 1, 2, 3
