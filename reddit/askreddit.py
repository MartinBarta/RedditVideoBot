from utils.console import print_markdown, print_step, print_substep
import praw
import random
from dotenv import load_dotenv
import os


def get_askreddit_threads():
    """
    Vrátí list threadů z AskReddit subredditu.
    """

    print_step("Získávám AskReddit thready...")

    content = {}
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="Accessing AskReddit threads",
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )
    askreddit = reddit.subreddit("askreddit")
    threads = askreddit.hot(limit=25)
    submission = list(threads)[random.randrange(0, 25)]
    print_substep(f"Video bude o: {submission.title} :thumbsup:")
    try:

        content["thread_url"] = submission.url
        content["thread_title"] = submission.title
        content["comments"] = []

        for top_level_comment in submission.comments:
            content["comments"].append(
                {
                    "comment_body": top_level_comment.body,
                    "comment_url": top_level_comment.permalink,
                    "comment_id": top_level_comment.id,
                }
            )

    except AttributeError as e:
        pass
    print_substep("Získal jsem AskReddit thready úspěšně.", style="bold green")
    return content
