{{ config(materialized='view') }}

select
    id,
    game_id,
    game_date::date as game_date,

    home_name  as home_team,
    home_score,
    away_name  as away_team,
    away_score,

    case
        when home_score > away_score then 1
        else 0
    end as home_win,

    case
        when away_score > home_score then 1
        else 0
    end as away_win
from {{ source('public_data', 'game') }}
where home_score is not null
  and away_score is not null