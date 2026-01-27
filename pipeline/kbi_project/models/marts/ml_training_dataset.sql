{{ config(materialized='table') }}

select
    game_id,
    game_date,
    home_win as target,

    home_avg_points_per_game,
    away_avg_points_per_game,
    home_goal_diff_per_game,
    away_goal_diff_per_game,

    home_avg_goals_for_5,
    home_avg_goals_against_5,
    away_avg_goals_for_5,
    away_avg_goals_against_5,
    home_win_rate_5,
    away_win_rate_5

    diff_avg_points_per_game,
    diff_win_rate_5,

    is_home

from {{ ref('fct_match_enriched') }}
where home_win is not null
