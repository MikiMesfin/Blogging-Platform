from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Category, Tag, Post, Comment
from django.utils import timezone
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Generates demo data for the blog'

    def handle(self, *args, **kwargs):
        # Create users
        self.stdout.write('Creating users...')
        users = []
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='demo1234',
                bio=fake.text()
            )
            users.append(user)

        # Create categories
        self.stdout.write('Creating categories...')
        categories = []
        for _ in range(5):
            category = Category.objects.create(
                name=fake.word().capitalize(),
                description=fake.text()
            )
            categories.append(category)

        # Create tags
        self.stdout.write('Creating tags...')
        tags = []
        for _ in range(10):
            tag = Tag.objects.create(name=fake.word())
            tags.append(tag)

        # Create posts
        self.stdout.write('Creating posts...')
        posts = []
        for _ in range(20):
            post = Post.objects.create(
                title=fake.sentence(),
                content=fake.paragraphs(3),
                author=random.choice(users),
                category=random.choice(categories),
                status=random.choice(['draft', 'published']),
                published_date=timezone.now() if random.choice([True, False]) else None
            )
            post.tags.set(random.sample(tags, random.randint(1, 3)))
            posts.append(post)

        # Create comments
        self.stdout.write('Creating comments...')
        for _ in range(50):
            Comment.objects.create(
                post=random.choice(posts),
                author=random.choice(users),
                content=fake.paragraph()
            )

        # Add likes
        self.stdout.write('Adding likes...')
        for post in posts:
            for _ in range(random.randint(0, 5)):
                post.likes.add(random.choice(users))

        self.stdout.write(self.style.SUCCESS('Successfully generated demo data')) 