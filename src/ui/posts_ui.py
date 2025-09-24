import questionary

from rich.markdown import Markdown
from rich.console import Console, Group
from rich.panel import Panel

from src.post import Post
from src.user import User

from src.ui.clean import clear_screen
from src.ui.header import header


class PostUI:
    def __init__(self, console: Console, author: User):
        self.console: Console = console
        self.author: User = author
        self.post: Post

    def add_post(self, post_type: str) -> Post | None:
        if post_type not in self.author.allowed_post_types:
            self.console.log(f"[FAIL] {self.author.name} can post {post_type}")
            questionary.press_any_key_to_continue().ask()
            return None

        title: str = questionary.text("Post title:", qmark="[···]").ask()

        content: str = questionary.text(
            "Post content:", qmark="[···]", multiline=True).ask()

        return Post(self.author, post_type, title, content)

    def update_content(self) -> bool:
        if self.post.author != self.author:
            self.console.log(
                f"[FAIL] {self.author.name} is not this post's author")
            questionary.press_any_key_to_continue().ask()
            return False

        content: str = questionary.text(
            "New content:", qmark="[···]", multiline=True).ask()

        self.post.content = content
        return True

    def like(self) -> bool:
        if self.post.user_liked(self.author.username):
            self.console.log(
                f"[FAIL] {self.author.name} already liked this post")
            questionary.press_any_key_to_continue().ask()
            return False

        self.post.like(self.author.username)
        return True

    def dislike(self) -> bool:
        if self.post.user_liked(self.author.username):
            self.post.dislike(self.author.username)
            return True

        self.console.log(f"[FAIL] {self.author.name} did not liked this post")
        questionary.press_any_key_to_continue().ask()
        return False

    def comment(self) -> bool:
        new_comment = self.add_post("comment")
        if new_comment:
            self.post.add_comment(new_comment)
            return True

        return False

    def show_comments(self) -> None:
        comments: list[Post] = self.post.comments
        self.show_posts(comments, False)
        return None

    def nothing(self) -> None:
        return None

    def post_actions(self, index: int) -> int:
        actions = {
            "Previous post": self.nothing,
            "Update": self.update_content,
            "Like": self.like,
            "Dislike": self.dislike,
            "Comment": self.comment,
            "Show comments": self.show_comments,
            "Next post": self.nothing
        }

        self.console.print()
        option = questionary.select("Choose an option:",
                                    choices=list(actions.keys())).ask()

        actions[option]()

        if option == "Next post":
            return index + 1
        elif option == "Previous post":
            return index - 1 if index > 0 else 0
        else:
            return index

    def show_posts(self, posts: list[Post], clear: bool):
        if len(posts) == 0:
            return None

        index = 0
        while index < len(posts):
            self.post = posts[index]

            if clear:
                clear_screen()
                self.console.print(header("SOCIAL FEED"))

            post_panel = Group(
                self.post.formatted_title(),
                Markdown(self.post.content),
                self.post.formatted_footer()
            )

            self.console.print(Panel(post_panel))
            self.console.print()

            index = self.post_actions(index)

        questionary.press_any_key_to_continue().ask()
        return None
