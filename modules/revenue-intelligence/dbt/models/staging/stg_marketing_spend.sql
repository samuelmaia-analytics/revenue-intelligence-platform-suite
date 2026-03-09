select
    cast(channel as {{ dbt.type_string() }}) as channel,
    cast(marketing_spend as {{ dbt.type_numeric() }}) as marketing_spend
from {{ source('raw', 'marketing_spend') }}
