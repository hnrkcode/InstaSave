import csv
import io
import os
from datetime import datetime

import magic
from PIL import Image


def check_path(output):
    """Create folder for downloaded files if it not exist."""

    if not os.path.isdir(output):
        os.makedirs(output)


def save_meta(data, output, index):
    """Save data from downloaded posts in a CSV file."""

    output = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(output))), "data.csv"
    )
    exists = os.path.isfile(output)

    # Data from posts.
    published = data["taken_at_timestamp"]
    data_scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.utcfromtimestamp(published).strftime("%Y-%m-%d")
    time = datetime.utcfromtimestamp(published).strftime("%H:%M:%S")

    post_type = data["__typename"]
    username = data["owner"]["username"]
    full_name = data["owner"]["full_name"]
    is_private = data["owner"]["is_private"]
    is_verified = data["owner"]["is_verified"]
    caption_is_edited = data["caption_is_edited"]
    comments_disabled = data["comments_disabled"]
    likes = data["edge_media_preview_like"]["count"]
    caption = data["edge_media_to_caption"]["edges"][0]["node"]["text"]

    title = None
    sub_type = None
    is_video = None
    duration = None
    comments = None
    shortcode = None
    access_cap = None
    product_type = None
    location_name = None
    sub_shortcode = None

    # Handle posts without location tag.
    try:
        location_name = data["location"]["name"]
    except TypeError:
        location_name = data["location"]

    # The key to the comment count number can be either of the two.
    try:
        comments = data["edge_media_to_parent_comment"]["count"]
    except KeyError:
        comments = data["edge_media_to_comment"]["count"]

    # Differentiate assignment depending on post type.
    if post_type == "GraphImage":
        is_video = data["is_video"]
        shortcode = data["shortcode"]
        access_cap = data["accessibility_caption"]

    elif post_type == "GraphVideo":
        title = data["title"]
        is_video = data["is_video"]
        shortcode = data["shortcode"]
        duration = data["video_duration"]
        product_type = data["product_type"]

    elif post_type == "GraphSidecar":
        node = data["edge_sidecar_to_children"]["edges"][index]["node"]
        sub_type = node["__typename"]
        sub_shortcode = node["shortcode"]
        is_video = node["is_video"]
        post_type = post_type
        shortcode = data["shortcode"]

        # Videos don't have accessibility caption.
        if sub_type != "GraphVideo":
            access_cap = node["accessibility_caption"]

        # Remember index in the sidecar, reset when done.
        edges = len(data["edge_sidecar_to_children"]["edges"])
        if index < edges - 1:
            index += 1
        else:
            index = 0

    # Append post data to the csv file.
    with open(output, "a") as csvfile:
        fieldnames = [
            "username",
            "full_name",
            "shortcode",
            "sub_shortcode",
            "type",
            "sub_type",
            "data_scraped_at",
            "published",
            "date",
            "time",
            "location_name",
            "accessibility_caption",
            "is_video",
            "video_duration",
            "product_type",
            "is_verified",
            "is_private",
            "likes",
            "comments",
            "comments_disabled",
            "caption_is_edited",
            "title",
            "caption",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Writes fieldname headers if it's the first time appending data.
        if not exists:
            writer.writeheader()

        writer.writerow(
            {
                "username": username,
                "full_name": full_name,
                "shortcode": shortcode,
                "sub_shortcode": sub_shortcode,
                "type": post_type,
                "sub_type": sub_type,
                "data_scraped_at": data_scraped_at,
                "published": published,
                "date": date,
                "time": time,
                "location_name": location_name,
                "accessibility_caption": access_cap,
                "is_video": is_video,
                "video_duration": duration,
                "product_type": product_type,
                "is_verified": is_verified,
                "is_private": is_private,
                "likes": likes,
                "comments": comments,
                "comments_disabled": comments_disabled,
                "caption_is_edited": caption_is_edited,
                "title": title,
                "caption": caption,
            }
        )

    return index


def save_file(buffer, output, filename):
    """Write content to file.

    Saves every file in a folder named after the uploaders in the output
    folder. Tries to remove any unvanted meta data from jpeg files
    and still keep the original quality. Mp4 files are unmodified.

    Args:
        buffer (bytes): File content in byte code.
        output (str): Where to save the file.
        filename (str): Name of the file.
    """

    check_path(output)

    # Look at the first 12 bytes to determine the file type,
    # because the first 4 bytes are needed for JPEGs and MP4 signatures
    # are 8 bytes long and are offset by 4 bytes, which means 12 bytes are
    # a minimum requirement in those cases.
    file_type = magic.from_buffer(buffer[:12], mime=True)

    if file_type == "image/jpeg":
        bytes = io.BytesIO(buffer)
        op = os.path.join(output, filename)
        # Save the image with Pillow to remove any unwanted meta data.
        # Also try to keep the same quality when saved.
        Image.open(bytes).save(op, quality="keep")
    elif file_type == "video/mp4":
        with open(os.path.join(output, filename), "wb") as f:
            f.write(buffer)
