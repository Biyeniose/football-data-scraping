# Web Scraping Scripts in Python on Ubuntu VPS
#### Run the scripts in Terminal/Shell

Run each individual Scraping scripts with Docker
```sh
docker-compose run --rm scraper python /app/scripts/scraper1.py 2
```
Logs are in the `logs\py_log.py` file

Or run with .sh script
```sh
./run_scraper_loop.sh 2 2024 2024
```
