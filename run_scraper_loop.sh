#!/bin/bash

league_id="$1"
start_year="$2"
end_year="$3"

current_year=$end_year

while [ "$current_year" -ge "$start_year" ]; do
  echo "Running command for year: $current_year"
  docker-compose run --rm scraper python /app/scripts/get_player_stats.py "$league_id" "$current_year"

  # Decrement the year for the next iteration
  current_year=$((current_year - 1))
done

echo "Finished processing years from $end_year down to $start_year."
