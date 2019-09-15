import functools
import uuid
from hashlib import blake2b


def unique_filename(func):
    """Return filename with an unique id appended to it's end."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        filename = func(*args, **kwargs)
        # Convert the random UUID to bytes.
        id = str.encode(str(uuid.uuid4()))
        # Convert the id to a 10 character long string.
        hash = blake2b(digest_size=10, key=id).hexdigest()
        # Separate the file extension from the name.
        filename = [filename[:-4], filename[-3:]]
        # Append the hash at the end of the name.
        filename[0] += "_" + hash
        # Merge the name and the file extension.
        filename = ".".join(filename)
        return filename

    return wrapper


def count_calls(func):
    """Count function calls."""

    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        if args[0].verbose:
            print(f"Post {wrapper_count_calls.num_calls}")
        else:
            print(".", end="", flush=True)
        return func(*args, **kwargs)

    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls
