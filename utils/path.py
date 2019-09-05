import io
import os

from PIL import Image


def save_file(buffer, output, filename):
    """Write content to file."""
    # Output path should be ~/[output]/[username]
    user_output = os.path.join(output, filename[:-52])
    # Create folder for downloaded files if it not exist.
    if not os.path.isdir(user_output):
        os.makedirs(user_output)
    # JPEG file signature always start with FF D8.
    # The other two bytes are FF Ex (x = 0-F).
    if buffer[:3] == b"\xff\xd8\xff" and (buffer[3] & 0xE0) == 0xE0:
        bytes = io.BytesIO(buffer)
        op = os.path.join(user_output, filename)
        # Save the image with Pillow to remove any unwanted meta data.
        # Also try to keep the same quality when saved.
        Image.open(bytes).save(op, quality="keep")
    # MP4 file signatures are 8 bytes long and are offset by 4 bytes.
    # The first four bytes are the same in both types of MP4 file formats.
    elif (
        buffer[4:8] == b"\x66\x74\x79\x70"
        and buffer[8:12] == b"\x69\x73\x6f\x6d"
        or buffer[8:12] == b"\x4d\x53\x4e\x56"
    ):
        with open(os.path.join(user_output, filename), "wb") as f:
            f.write(buffer)
