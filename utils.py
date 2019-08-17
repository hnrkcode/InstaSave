import random
from settings import USER_AGENT_FILE

def random_useragent():
    """Read in all possible user agents from a file and pick one."""

    filename = USER_AGENT_FILE

    with open(filename, 'r') as f:
        # Read the file and split it's lines into a list of user agents.
        lines = f.read().splitlines()
        # Randomly pick one user agent from the list.
        user_agent = random.choice(lines)

    f.close()

    return user_agent
