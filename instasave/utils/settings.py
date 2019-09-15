import os.path

# Projects absolute path.
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# Path to the "data" directory.
DATA_DIR = os.path.join(BASE_DIR, "data")

# Text file with a list of different user agents.
USER_AGENT_FILE = os.path.join(DATA_DIR, "useragents.txt")

# Web driver for selenium.
GECKODRIVER = os.path.join(DATA_DIR, "geckodriver")
