with matches as (
    
    select * from {{ ref('fct_matches') }}
    where league = 'RFPL'
    and season = 2025
    and home_goals is not NULL

),

teams as (

    select * from {{ ref('dim_teams') }}

),

full_match_table as (

    select
        m.match_id,
        m.league,
        m.season,
        m.match_date,
        m.match_time,
        t1.name as home_team_name,
        t2.name as away_team_name,
        m.home_goals,
        m.away_goals,
        m.home_xg,
        m.away_xg
    
    from matches as m
    left join teams as t1 on m.home_team_id = t1.id
    left join teams as t2 on m.away_team_id = t2.id
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
    from full_match_table

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
    from full_match_table

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
    w + d + l as gp,
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