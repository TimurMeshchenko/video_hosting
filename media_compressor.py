from moviepy.editor import VideoFileClip
from PIL import Image

def compress_video(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    video_clip.write_videofile(output_file, bitrate='1000k')
    video_clip.close()

def compress_image(input_image, output_image, quality=25):
    with Image.open(input_image) as img:
        img.save(output_image, quality=quality, optimize=True)

input_file = 'minecraft.mp4'
output_file = 'compressed_video.mp4'
compress_video(input_file, output_file)

input_image = 'minecraft.jpg'
output_image = 'compressed_image.jpg'
compress_image(input_image, output_image)