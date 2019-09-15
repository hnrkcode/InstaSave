def private_profile(data):
    if "entry_data" in data:
        return data["entry_data"]["ProfilePage"][0]["graphql"]["user"][
            "is_private"
        ]
    return data


def hashtag_post_count(data):
    if "entry_data" in data:
        return data["entry_data"]["TagPage"][0]["graphql"]["hashtag"][
            "edge_hashtag_to_media"
        ]["count"]
    return data


def user_post_count(data):
    if "entry_data" in data:
        return data["entry_data"]["ProfilePage"][0]["graphql"]["user"][
            "edge_owner_to_timeline_media"
        ]["count"]
    return data


def shortcode_media(data):
    if "entry_data" in data:
        return data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
    return data
