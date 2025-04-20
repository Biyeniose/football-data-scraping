import re, requests, sys, json, random, os, re
from datetime import datetime

def convert_to_minutes(time_string):
    """
    Converts a time string in the format "X.XXX'" to minutes (float).

    Args:
        time_string (str): The time string to convert.

    Returns:
        float: The time in minutes, or None if the input is invalid.
    """
    try:
        if "'" in time_string:
            minutes = time_string.replace("'", "")
            minutes2 = float(minutes.replace(".", ""))
            return minutes2
        
        elif time_string == "-":
            return 0
        else:
            return None  # Invalid format
    except ValueError:
        return None  # Invalid number format
