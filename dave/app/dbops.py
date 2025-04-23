import pdb

from typing import Generator, List
from io import BytesIO

from flask import abort
import sqlalchemy as sa

from app.models import User, TextHTML, Image, ImageType
from app.tools import generate_random_label
from app.extensions import db


class DBOps:
    @staticmethod
    def create_user(
        username: str,
        email: str,
        password: str,
        repeat_password: str
    ) -> User | None:
        if password != repeat_password:
            return None
        user = DBOps.get_user_by_username(username)
        if user:
            return None
        user = DBOps.get_user_by_email(email)
        if user:
            return None
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(this_id: int) -> User:
        user = User.query.filter_by(id=this_id).first()
        return user

    @staticmethod
    def get_user_by_username(this_username: str) -> User | None:
        user = User.query.filter_by(username=this_username).first()
        return user

    @staticmethod
    def get_user_by_email(this_email: str) -> User | None:
        user = User.query.filter_by(email=this_email).first()
        return user

    @staticmethod
    def check_token(token: str) -> User | None:
        user = db.session.scalar(sa.select(User).where(User.token == token))
        if user is None or user.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        else:
            return user

    @staticmethod
    def delete_user(this_id: int) -> None:
        user = DBOps.get_user_by_id(this_id)
        if user:
            user.delete()
            db.session.commit()
        else:
            message = f"DBOps.delete_user: User.id == {this_id} doesn't exist"
            raise LoggedException(message)

    @staticmethod
    def create_text_html(
        content: str,
        author: User
    ) -> TextHTML:
        label = generate_random_label()
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
        image_content: BytesIO,
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
