select
    cast(customer_id as {{ dbt.type_int() }}) as customer_id,
    cast(signup_date as {{ dbt.type_date() }}) as signup_date,
    cast(channel as {{ dbt.type_string() }}) as channel,
    cast(segment as {{ dbt.type_string() }}) as segment
from {{ source('raw', 'customers') }}
