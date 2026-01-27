{{ config(materialized='view') }}

select
    row_date::date as row_date,
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
from {{ source('public_data', 'table') }}