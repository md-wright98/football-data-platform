with home as (

    select 
        home_team_id as id,
        home_team_name as name,
        home_team_name_short as short_name
    
    from {{ ref('stg_understat__matches') }} 

),

away as (

    select 
        away_team_id as id,
        away_team_name as name,
        away_team_name_short as short_name
    
    from {{ ref('stg_understat__matches') }} 

),

combined as (

    select * from home

    union all

    select * from away

)

select 
    distinct(id),
    name,
    short_name
from combined