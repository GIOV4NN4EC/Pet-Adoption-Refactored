from rich.console import Console

from src.post import Post
from src.user import User

from src.ui.menus.menu import Menu
from src.ui.posts_ui import PostUI


class SocialMenu(Menu):
    def __init__(self, user: User, console: Console):
        Menu.__init__(self, user, console)

        self.name = "social menu"
        self.social_feed = PostUI(console, user)

        self.actions = {
            "Return to Main Menu":
                {"func": self.go_back,
                 "args": []},

            "Show Feed":
                {"func": self.show_posts,
                 "args": []},

            "Add Forum Post":
                {"func": self.social_feed.add_post,
                 "args": ["forum"]},

            "Add Educational Post":
                {"func": self.social_feed.add_post,
                 "args": ["educational"]},

            "Add Succes Story Post":
                {"func": self.social_feed.add_post,
                 "args": ["success story"]}
        }

    def show_posts(self):
        posts = list(Post.data.values())
        self.social_feed.show_posts(posts, True)
