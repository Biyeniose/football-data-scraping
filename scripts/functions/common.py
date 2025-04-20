import re, requests, sys, json, random, os, re
from bs4 import BeautifulSoup
from datetime import datetime
from scripts.utils.supabase_cli import supabase
from scripts.utils.time_convert import convert_to_minutes
from termcolor import colored, cprint

def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
    }
    response = requests.get(url, headers=headers).content
    soup = BeautifulSoup(response, "html.parser")
    return soup

def get_page_trs(soup):
    trs_odd = soup.find_all('tr', class_="odd")
    trs_even = soup.find_all('tr', class_="even")
    return trs_odd + trs_even



