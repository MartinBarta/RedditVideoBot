from playwright.sync_api import sync_playwright
from pathlib import Path
from rich.progress import track
from utils.console import print_step, print_substep


def download_screenshots_of_reddit_posts(reddit_object, screenshot_num):
    """Stáhne screenshoty z reddit postu tak jak jdou za sebou.

    Args:
        reddit_object: Reddit object v askreddit.py
        screenshot_num: Číslo screenshotů které checeme stáhnout.
    """
    print_step("Stahuji screenshoty z Reddit postu 📷")

    # ! Ujistí se že složka na ukládání reddit screenshotů existuje
    Path("assets/png").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print_substep("Launchuji neviditelný prohlížeč...")

        browser = p.chromium.launch()

        # Získá screenshoty threadu
        page = browser.new_page()
        page.goto(reddit_object["thread_url"])

        if page.locator('[data-testid="content-gate"]').is_visible():
            # Klikne na tlačítko POVOLIT aby se mohl dostat k NSFW threadu pokud byl nalezen.

            print_substep("Tento post je NSFW. Pozor na to kam ho dáváš... :fire:")
            page.locator('[data-testid="content-gate"] button').click()

        page.locator('[data-test-id="post-content"]').screenshot(
            path="assets/png/title.png"
        )

        for idx, comment in track(
            enumerate(reddit_object["comments"]), "Stahuji screenshoty..."
        ):

            # Zastaví se jakmile jsme dostali -> screenshot_num
            if idx >= screenshot_num:
                break

            if page.locator('[data-testid="content-gate"]').is_visible():
                page.locator('[data-testid="content-gate"] button').click()

            page.goto(f'https://reddit.com{comment["comment_url"]}')
            page.locator(f"#t1_{comment['comment_id']}").screenshot(
                path=f"assets/png/comment_{idx}.png"
            )
        print_substep("Screenshoty byly úspěšně staženy.", style="bold green")
