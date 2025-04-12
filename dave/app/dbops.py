from typing import IO, BinaryIO

from flask import abort

from models import User, TextHTML, Image
from tools import create_key
from . import db


class DBOps:
    @staticmethod
    def create_user(
        username: str,
        email: str,
        password: str,
        repeat_password: str
    ) -> User | None
        if password != repeat_password:
            return None
        else:
            user = User(username, email)
            user.set_password(password)
            db.session.add(user)
            db.commit()
            return user

    @staticmethod
    def get_user(id: int) -> User:
        return User.query.get_or_404(id)

    @staticmethod
    def look_for_user(
        username: str | None = None,
        email: str | None
    ) -> User | None
        if username:
            # user = db.first_or_404(sa.select(User).where(User.username == username))
            return User.query.filter_by(username=username).first_or_404()
        if email:
            return User.query.filter_by(email=email).first_or_404()
        return None

    @staticmethod
    def delete_user(id: int):
        user = User.query.get_or_404(id)
        user.delete()
        db.session.commit()

    @staticmethod
    def create_text_html(
        content: str,
        author: User
    ) -> TextHTML:
        label = create_label()
        row = TextHTML(label=label, content=content, author=author)
        db.session.add(row)
        db.commit()
        return row

    @staticmethod
    def look_for_text_html(
        label: str | None = None,
        content: str | None = None,
        author: User | None = None,
        batch_size: int = 100
    ) -> Generator[TextHTML, None, None]:
        if label:
            row = TextHTML.query.filter_by(label=label).first_or_404()
            yield row
        elif content:
            query = TextHTML.query.filter_by(TextHTML.content.contains(content))
            for row in query.yield_per(100):
                yield row
        elif author:
            for row in author.text_htmls:
                yield row
        else:
            yield from ()

    @staticmethod
    def delete_text_html(id: int) -> None:
        text_html = TextHTML.query.get_or_404(id)
        text_html.delete()
        db.session.commit()

    @staticmethod
    def create_image(
        image_content: BInaryIO[IO[bytes]],
        image_type: ImageType,
        author: User
    ) -> Image:
        label = create_label()
        cursor = db.session.query(Image).count()
        image = Image(label=label, cursor=cursor, image_type=image_type, author=author)
        db.session.add(image)
        db.session.commit()
        filepath = image.filepath()
        image_content.save(filepath)
        return image

    @staticmethod
    def look_for_image(
        label: str | None = None,
        author: User | None = None
    ) -> List[Image]:
        if label:
            row = Image.query.filter_by(label=label).first_or_404()
            yield row
        elif author:
            for row in author.images:
                yield row
        else:
            yield from ()

    @staticmethod
    def delete_image(id: int) -> None:
        row = Image.query.get_or_404(id)
        filepath = row.filepath()
        os.remove(filepath)
        row.delete()
        db.session.commit()
