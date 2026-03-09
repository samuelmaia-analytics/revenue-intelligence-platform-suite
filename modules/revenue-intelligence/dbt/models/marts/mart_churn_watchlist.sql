with customer_lifetime as (
    select * from {{ ref('int_customer_lifetime') }}
)

select
    customer_id,
    channel,
    segment,
    lifetime_revenue,
    total_orders,
    last_order_date,
    case
        when last_order_date < {{ dbt.dateadd('day', -90, 'current_date') }} then 'high'
        when last_order_date < {{ dbt.dateadd('day', -45, 'current_date') }} then 'medium'
        else 'low'
    end as churn_risk_band
from customer_lifetime
