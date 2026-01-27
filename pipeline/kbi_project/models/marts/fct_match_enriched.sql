{{ config(materialized='table') }}

select
    g.game_id,
    g.game_date,

    g.home_team,
    g.away_team,

    g.home_win,

    h.win_rate_last_5               as home_win_rate_5,
    a.win_rate_last_5               as away_win_rate_5,

    h.avg_goals_for_last_5          as home_avg_goals_for_5,
    h.avg_goals_against_last_5      as home_avg_goals_against_5,

    a.avg_goals_for_last_5          as away_avg_goals_for_5,
    a.avg_goals_against_last_5      as away_avg_goals_against_5,

    hc.points::float / nullif(hc.games_played, 0)
        as home_avg_points_per_game,

    ac.points::float / nullif(ac.games_played, 0)
        as away_avg_points_per_game,

    hc.goal_differential::float / nullif(hc.games_played, 0)
        as home_goal_diff_per_game,

    ac.goal_differential::float / nullif(ac.games_played, 0)
        as away_goal_diff_per_game,

    (hc.points::float / nullif(hc.games_played, 0))
      - (ac.points::float / nullif(ac.games_played, 0))
        as diff_avg_points_per_game,

    h.win_rate_last_5 - a.win_rate_last_5
        as diff_win_rate_5,

    1 as is_home

from {{ ref('stg_game') }} g

left join {{ ref('fct_team_form') }} h
  on h.team = g.home_team
 and h.game_date = g.game_date

left join {{ ref('fct_team_form') }} a
  on a.team = g.away_team
 and a.game_date = g.game_date

left join {{ ref('dim_team_current') }} hc
  on hc.team_abbrev = g.home_team

left join {{ ref('dim_team_current') }} ac
  on ac.team_abbrev = g.away_team
