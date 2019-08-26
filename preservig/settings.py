import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

# Text file with a list of different user agents.
USER_AGENT_FILE = os.path.join(DATA_DIR, "useragents.txt")

# The date format used by Instagram on feed posts.
POST_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
