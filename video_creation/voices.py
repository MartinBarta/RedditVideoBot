from gtts import gTTS
from pathlib import Path
from mutagen.mp3 import MP3
from utils.console import print_step, print_substep
from rich.progress import track


def save_text_to_mp3(reddit_obj):
    """Ukládá text do MP3 souboru.

    Args:
        reddit_obj : RedditAPI v askreddit.py souboru.
    """
    print_step("Ukládám text do MP3 souboru 🎶")
    length = 0

    # Vytvoří složku pro MP3 soubory.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    tts = gTTS(text=reddit_obj["thread_title"], lang="en-uk", slow=False, tld="co.uk")
    tts.save(f"assets/mp3/title.mp3")
    length += MP3(f"assets/mp3/title.mp3").info.length

    for idx, comment in track(enumerate(reddit_obj["comments"]), "Ukládám..."):
        # ! Přestane převádět text na MP3 pokud je delší jak 50 sekund. Může to být delší, ale tohle je dobrý začátek
        if length > 50:
            break
        tts = gTTS(text=comment["comment_body"], lang="en-uk")
        tts.save(f"assets/mp3/{idx}.mp3")
        length += MP3(f"assets/mp3/{idx}.mp3").info.length

    print_substep("Text byl do MP3 souboru úspěšně uložen.", style="bold green")
    # ! Vrátí index abysme věděli kolik screenshotů od komentářů máme udělat.
    return length, idx
