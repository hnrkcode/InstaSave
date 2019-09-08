import io
import os

from PIL import Image


# def save_file(buffer, output, filename, date, shortcode):
def save_file(buffer, output, filename):
    """Write content to file.

    Saves every file in a folder named after the uploaders in the output
    folder. Tries to remove any unvanted meta data from jpeg files
    and still keep the original quality. Mp4 files are unmodified.

    Args:
        buffer (bytes): File content in byte code.
        output (str): Where to save the file.
        filename (str): Name of the file.
        shortcode (str): Save post in folder named after the post's shortcode.
    """

    # Create folder for downloaded files if it not exist.
    if not os.path.isdir(output):
        os.makedirs(output)
    # JPEG file signature always start with FF D8.
    # The other two bytes are FF Ex (x = 0-F).
    if buffer[:3] == b"\xff\xd8\xff" and (buffer[3] & 0xE0) == 0xE0:
        bytes = io.BytesIO(buffer)
        op = os.path.join(output, filename)
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
        with open(os.path.join(output, filename), "wb") as f:
            f.write(buffer)
