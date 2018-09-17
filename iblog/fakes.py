from iblog.models import Admin, Category
from iblog.extensions import db
from faker import Faker
from sqlalchemy.exc import IntegrityError
import random

faker = Faker()


def fake_posts(count=50):
    for i in range(count):
        poist = Post(
            title=fake.sentence(),
            body=fake.text(1500),
            category=Category.query.get(
                random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for in in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='iBlog',
        blog_sub_title='a blog app built on Flask',
        name='Peter Dinklage',
        about='You need write something here...'
    )
    admin.set_password('flaskiscool')
    db.session.add(admin)
    db.session.commit()
