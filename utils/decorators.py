def start_at_shortcode_media(func):
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        # Return data from this position in the dict.
        return data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
    return wrapper
