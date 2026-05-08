{{ config(
    materialized='table'
) }}

with raw as (

    select * from {{ source('understat', 'understat_matches_raw') }}

),

flattened as (

    select 
        match_id,
        league,
        json_value(payload, "$.h.id") AS home_team_id,
        json_value(payload, "$.h.title") AS home_team_name,
        json_value(payload, "$.h.short_title") AS home_team_name_short,
        json_value(payload, "$.a.id") AS away_team_id,
        json_value(payload, "$.a.title") AS away_team_name,
        json_value(payload, "$.a.short_title") AS away_team_name_short,
        safe_cast(json_value(payload, "$.goals.h") as int64) as home_goals,
        safe_cast(json_value(payload, "$.goals.a") as int64) as away_goals,
        safe_cast(json_value(payload, "$.xG.h") as float64) as home_xg,
        safe_cast(json_value(payload, "$.xG.a") as float64) as away_xg,
        cast(timestamp(json_value(payload, '$.datetime')) as date) as match_date,
        cast(timestamp(json_value(payload, '$.datetime')) as time) as match_time,
        safe_cast(json_value(payload, "$.forecast.w") as float64) as home_win_probability,
        safe_cast(json_value(payload, "$.forecast.d") as float64) as draw_probability,
        safe_cast(json_value(payload, "$.forecast.l") as float64) as away_win_probability,
    from raw
    qualify row_number() over (partition by match_id order by extracted_at desc) = 1

)

select * from flattened