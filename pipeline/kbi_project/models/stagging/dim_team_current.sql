{{ config(materialized='table') }}

with ranked as (
    select *,
           row_number() over (
               partition by team_abbrev
               order by row_date desc
           ) as rn
    from {{ ref('stg_team_standings') }}
)

select
    team_abbrev,
    team_name,
    conference,
    division,
    games_played,
    wins,
    losses,
    ot_losses,
    points,
    point_percentage,
    goals_for,
    goals_against,
    goal_differential,
    conference_rank,
    division_rank,
    league_rank
from ranked
where rn = 1