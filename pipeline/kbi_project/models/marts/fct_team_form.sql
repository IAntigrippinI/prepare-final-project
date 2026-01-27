{{ config(materialized='table') }}

with games as (

    select
        game_date,
        home_team as team,
        home_score as goals_for,
        away_score as goals_against,
        home_win as win
    from {{ ref('stg_game') }}

    union all

    select
        game_date,
        away_team as team,
        away_score as goals_for,
        home_score as goals_against,
        away_win as win
    from {{ ref('stg_game') }}

),

rolling as (
    select
        team,
        game_date,

        round(avg(win) over (
            partition by team
            order by game_date
            rows between 4 preceding and current row
        ), 4) as win_rate_last_5,

        round(avg(goals_for) over (
            partition by team
            order by game_date
            rows between 4 preceding and current row
        ), 4) as avg_goals_for_last_5,

       round(avg(goals_against) over (
            partition by team
            order by game_date
            rows between 4 preceding and current row
        ), 4) as avg_goals_against_last_5

    from games
)

select * from rolling