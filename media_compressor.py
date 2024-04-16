from moviepy.editor import VideoFileClip
from PIL import Image
import os

def compress_video(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    video_clip.write_videofile(output_file, bitrate='1000k')
    video_clip.close()

def compress_image(input_image, output_image, quality=25):
    with Image.open(input_image) as img:
        img.save(output_image, quality=quality, optimize=True)

def get_files_in_dir(base_directory, take_from_directory_name):
    directory = os.path.join(base_directory, take_from_directory_name)
    files = os.listdir(directory)
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        # output_file = file_name.replace("SaveTube.io-", "").replace("_", "").replace("  ", " ")
        # compressed_directory = os.path.join(base_directory, get_filename_without_extension(output_file))
        # file_compressed_path = os.path.join(compressed_directory, output_file)
        # os.makedirs(compressed_directory, exist_ok=True)
        # if file_name.endswith('mp4'):
        #     compress_video(file_path, file_compressed_path)
        # elif file_name.endswith('jpg'):
            # compress_image(file_path, file_compressed_path)
        try:
            compress_image(file_path, file_path)
        except Exception:
            print("!!! failed")
            print(file_name)

def get_files_in_dir_dir(base_directory):
    directory = os.listdir(base_directory)
    for folder_name in directory:
        folder = os.path.join(base_directory, folder_name)
        files = os.listdir(folder)
        for file_name in files:
            file_path = os.path.join(folder, file_name)
            compress_image(file_path, file_path)

def get_filename_without_extension(filename: str):
    filename_with_extension = filename.split('/')[-1]
    filename_parts = filename_with_extension.split('.')
    filename_without_extension = '.'.join(filename_parts[:-1])
    return filename_without_extension

get_files_in_dir("media_compressed", "")
# get_files_in_dir_dir("media_compressed")
