from src.model import Model
from src.user import User

# import textwrap


class Post(Model):
    def __init__(self, author: User, post_type: str,
                 title: str, content: str):
        if post_type not in author.allowed_post_types:
            raise Exception(f"{author.username} can't post {post_type}")

        self.__author: User = author
        self.__post_type: str = post_type
        self.__title: str = title
        self.__content: str = content

        self.__comments: list['Post'] = []
        self.__likes: list[str] = []

        self.data[title] = self

    @property
    def author(self) -> str:
        return self.__author.username

    @property
    def title(self) -> str:
        return self.__title

    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, new_content: str) -> None:
        if len(new_content) == 0:
            raise ValueError("New content can't be empty")

        self.__content = new_content

    @property
    def comments(self) -> list['Post']:
        return self.__comments

    def add_comment(self, new_comment: 'Post') -> None:
        self.__comments.append(new_comment)

        return None

    @property
    def likes(self) -> int:
        """returns only the ammount of likes"""

        return len(self.__likes)

    def user_liked(self, u: str) -> bool:
        return u in self.__likes

    def like(self, liker: str) -> None:
        if self.user_liked(liker):
            raise ValueError("this user already liked this post")

        self.__likes.append(liker)
        return None

    def dislike(self, liker: str) -> None:
        if self.user_liked(liker):
            self.__likes.remove(liker)
            return None

        raise ValueError("this user did not liked this post")

    def formatted_title(self) -> str:
        title: str = f"{self.__post_type.title()} post by "
        title += f"{self.__author.name.title()} ({self.__author})"
        title += f"\nᯓ➤ {self.__title.upper()}\n"

        return title

    def formatted_footer(self) -> str:
        return f"\n:speech_balloon: {len(self.__comments)} commentss :heart: {self.likes} likes"

    def __str__(self) -> str:
        return f"{self.__post_type} by {self.__author}"

    def formatted_list(self) -> list[str]:
        """Generates a list of strings with the post's info formatted"""

        post_info: list[str] = []

        post_info.append(f"{self.__post_type.title()} post by "
                         + f"{self.__author.name.title()} ({self.__author})")

        post_info.append(f"\nᯓ➤ {self.__title.upper()}")
        post_info.append("")
        # post_info.extend(textwrap.wrap(self.__content,
        #                                initial_indent="  ╰┈➤ ",
        #                                subsequent_indent="      "))
        post_info.append(self.__content)
        post_info.append("")
        post_info.append(
            f"  :speech_balloon: {len(self.__comments)} commentss :heart: {self.likes} likes")

        return post_info
