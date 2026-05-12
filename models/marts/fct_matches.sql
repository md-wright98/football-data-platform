with raw as (

    select * from {{ ref('stg_understat__matches') }}

)

select 
    match_id,
    league,
    season,
    match_date,
    match_time,
    home_team_id,
    away_team_id,
    home_goals,
    away_goals,
    home_xg,
    away_xg
from raw