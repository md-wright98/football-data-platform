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
        json_value(payload, "$.goals.h") as home_goals,
        json_value(payload, "$.goals.a") as away_goals,
        json_value(payload, "$.xG.h") as home_xg,
        json_value(payload, "$.xG.a") as away_xg,
        cast(timestamp(json_value(payload, '$.datetime')) as date) as match_date,
        cast(timestamp(json_value(payload, '$.datetime')) as time) as match_time,
        json_value(payload, "$.forecast.w") as home_win_probability,
        json_value(payload, "$.forecast.d") as draw_probability,
        json_value(payload, "$.forecast.l") as away_win_probability,
    from raw

)

select * from flattened