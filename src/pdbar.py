"""
MIT License

Copyright (c) 2025 John Riggles [sudo_whoami]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime as dt
from asyncio import run

import feedparser as fp
import rumps


class PDBar(rumps.App):
    def __init__(self) -> None:
        """Show the Pixel Dailies theme in the menu bar (as app's title)"""
        super().__init__('PDBar', menu=['Pixel Dailies', 'Refresh'])
        # refresh every hour (3600 seconds)
        rumps.Timer(self.refresh, 3600).start()
        self.latest_tag: str | None = None

    @rumps.clicked('Refresh')
    def refresh(self, _sender=None) -> None:
        """Manually refresh on menu item click"""
        run(self._refresh_handler())

    async def _refresh_handler(self) -> None:
        """Handle running `self.get_tag` asynchronously"""
        self.title = 'Refreshing...'
        self.title = await self.get_tag()
        self.notify_on_change()

    def notify_on_change(self) -> None:
        """Check to see if the tag has been updated, notify on changes"""
        if self.title != self.latest_tag:
            timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            rumps.notification(
                title='Pixel Dailies Theme:',
                subtitle=f'{self.title}',
                message=f'Last checked at {timestamp}',
                action_button='Close',
            )
        # store the latest tag for comparison later
        self.latest_tag = self.title

    @staticmethod
    async def get_tag() -> str:
        """Parse `'https://lospec.com/dailies/'` for the tag of the day

        Returns:
            str: the tag of the day `#tag` -or-
            str: `No Tag Found` if no tag is found -or-
            str: `Error: <HTTP status code>` for any response code other
            than 200
        """
        URL = 'https://mastodon.art/@Pixel_Dailies.rss'
        feed = fp.parse(URL)
        tag = [
            tag['term']
            for tag in feed.entries[0].tags
            if tag['term'] != 'pixel_dailies'
        ]
        return f'#{tag[0]}' if tag else 'No Tag Found'


if __name__ == '__main__':
    app = PDBar()
    app.run()
