import json
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def random_user_agent():
    """Read in all possible user agents from a file and pick one."""

    filename = "useragents.txt"

    with open(filename, 'r') as f:
        # Read the file and split it's lines into a list of user agents.
        lines = f.read().splitlines()
        # Randomly pick one user agent from the list.
        user_agent = random.choice(lines)

    f.close()

    return user_agent

def get_post_data(url):
    """Returns the file URLs and the post type."""

    # Add a random user agent to the request HTTP headers to hide it's a script.
    headers = {"User-Agent": random_user_agent()}
    # Get the page's HTML code and parse it with BeautifulSoup to find the type
    # of the post.
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    data = json.loads(soup.select("script[type='text/javascript']")[3].text[21:-1])
    post_type = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]

    # Post with a video file.
    if post_type == "GraphVideo":
        image_url = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"]
    # Post with a image file.
    elif post_type == "GraphImage":
        image_url = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]
    # Post with multiple files, either images and/or videos.
    elif post_type == "GraphSidecar":
        edges = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
        # Differentiate between images and videos in multi-content posts.
        # Get urls with .jpg for images and .mp4 for videos.
        image_url = [edge["node"]["video_url"] if edge["node"]["__typename"] == "GraphVideo" else edge["node"]["display_url"] for edge in edges]

    return image_url, post_type

def save(content, filename):
    """Write content to file."""
    with open(filename, 'wb') as f:
        f.write(content)
    f.close()

def pick_filename(headers):
    """Give the file a unique name."""
    # Get the date the post was uploaded.
    d = datetime.strptime(headers.get('last-modified'), "%a, %d %b %Y %H:%M:%S %Z")
    # Format the date and time and use it in the filename.
    filename = d.strftime("%Y%m%d_%H%M%S_")
    # Add a unique string to the filename to prevent conflicting names.
    filename += headers.get('x-enc-origin-req-handler')
    # Add file extension based on the contents type.
    if headers.get('content-type') == "video/mp4":
        filename += ".mp4"
    else:
        filename += ".jpg"

    return filename

def download_file(url):
    """Get the content from the url, pick a name for the file and save it."""
    r = requests.get(url)
    filename = pick_filename(r.headers)
    save(r.content, filename)

def download(data):
    """Download files to disk."""
    post_urls = data[0]
    post_type = data[1]

    # Post with a video file.
    if post_type == "GraphVideo":
        download_file(post_urls)
    # Post with a image file.
    elif post_type == "GraphImage":
        download_file(post_urls)
    # Post with multiple files, either images and/or videos.
    elif post_type == "GraphSidecar":
        for url in post_urls:
            download_file(url)

if __name__ == '__main__':
    #data = get_post_data("https://www.instagram.com/p/B1Ele5pAHmg/") # mp4
    data = get_post_data("https://www.instagram.com/p/B1HDnV8ge0W/?utm_source=ig_web_options_share_sheet") # jpg
    #data = get_post_data("https://www.instagram.com/p/B0WpFNdg40t/") # multi
    print(data)
    download(data)
