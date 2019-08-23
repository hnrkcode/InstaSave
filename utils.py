import random

def random_useragent(filename):
    """Read in all possible user agents from a file and pick one."""

    try:
        with open(filename, 'r') as f:
            # Read the file and split it's lines into a list of user agents.
            lines = f.read().splitlines()
            # Randomly pick one user agent from the list.
            user_agent = random.choice(lines)
    except FileNotFoundError as e:
        raise SystemExit(f"{e.args[1]}: {filename}") from None

    return user_agent
