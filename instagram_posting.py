from instagrapi import Client
from instagrapi.types import Usertag, Location
import config
from pathlib import Path


def post_to_instagram(caption,image_path):
    cl = Client()
    cl.login(config.username, config.password)
    user = cl.user_info_by_username("CapGenius")

    image_path  = Path(image_path)

    media = cl.photo_upload(
        path=image_path,
        caption=caption,
        usertags=[Usertag(user=user, x=0.5, y=0.5)],
        # location=Location(lat=48.858844300000001, lng=2.2943506, name="Toronto"),
        extra_data={
            "custom_accessibility_caption": "alt text example",
            "like_and_view_counts_visible": False,
            "disable_comments": False,
            }
    )


