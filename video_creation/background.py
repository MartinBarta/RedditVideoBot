from random import randrange
from pytube import YouTube
from pathlib import Path
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
from utils.console import print_step, print_substep


def get_start_and_end_times(video_length, length_of_clip):

    random_time = randrange(180, int(length_of_clip) - int(video_length))
    return random_time, random_time + video_length


def download_background():
    """Stáhne video v pozadí z youtube.

    """

    if not Path("assets/mp4/background.mp4").is_file():
        print_step(
            "Musíme stáhnout video na pozadí z Minecraftu. Je to poměrně velké, ale stahuje se jen jednou. 😎"
        )
        print_substep("Stahuji video co bude na pozadí... prosím vydržte! 🙏")
        YouTube("https://www.youtube.com/watch?v=n_Dv4JMiwK8").streams.filter(
            res="720p"
        ).first().download(
            "assets/mp4",
            filename="background.mp4",
        )
        print_substep("Video do pozadí bylo úspěšně staženo! 🎉", style="bold green")


def chop_background_video(video_length):
    print_step("Hledám kousek ve videu který bych mohl střihnout...✂️")
    background = VideoFileClip("assets/mp4/background.mp4")

    start_time, end_time = get_start_and_end_times(video_length, background.duration)
    ffmpeg_extract_subclip(
        "assets/mp4/background.mp4",
        start_time,
        end_time,
        targetname="assets/mp4/clip.mp4",
    )
    print_substep("Kousek z videa v pozadí byl úspěšně vystřižen! 🎉", style="bold green")
