with epl_raw as (
    
    select * from {{ ref('stg_understat__matches') }}
    where league = 'EPL'
    and season = 2025
    and home_goals is not NULL

),

home_results as (

    select
        home_team_name as team_name,
        "home" as home_away,
        home_goals AS team_goals,
        home_xg AS team_xg,
        away_goals AS opposition_goals,
        away_xg AS opposition_xg,
        case
            when home_goals > away_goals then 1
            when home_goals = away_goals then 0
            else 0
            end as wins,
        case
            when home_goals > away_goals then 0
            when home_goals = away_goals then 1
            else 0
            end as draws,
        case
            when home_goals > away_goals then 0
            when home_goals = away_goals then 0
            else 1
            end as losses,
        case
            when home_goals > away_goals then 3
            when home_goals = away_goals then 1
            else 0
            end as points
    from epl_raw

),

away_results as (

    select
        away_team_name as team_name,
        "away" as home_away,
        away_goals AS team_goals,
        away_xg AS team_xg,
        home_goals AS opposition_goals,
        home_xg AS opposition_xg,
        case
            when home_goals < away_goals then 1
            when home_goals = away_goals then 0
            else 0
            end as wins,
        case
            when home_goals < away_goals then 0
            when home_goals = away_goals then 1
            else 0
            end as draws,
        case
            when home_goals < away_goals then 0
            when home_goals = away_goals then 0
            else 1
            end as losses,
        case
            when home_goals < away_goals then 3
            when home_goals = away_goals then 1
            else 0
            end as points
    from epl_raw

),

combined_results as (

    select * from home_results

    union all

    select * from away_results

),

final as (

    select
        team_name,
        sum(wins) AS w,
        sum(draws) AS d,
        sum(losses) AS l,
        sum(points) as pts,
        sum(team_goals) AS gf,
        sum(opposition_goals) as ga,
        sum(team_goals) - sum(opposition_goals) as gd,
        round(sum(team_xg), 2) as xg_for,
        round(sum(opposition_xg), 2) as xg_ag,

    from combined_results
    group by team_name

)

select 
    row_number() over(order by pts desc, gd desc, gf desc) as pos,
    team_name,
    w,
    d,
    l,
    pts,
    gf,
    ga,
    gd,
    xg_for,
    xg_ag 
from final
order by pos