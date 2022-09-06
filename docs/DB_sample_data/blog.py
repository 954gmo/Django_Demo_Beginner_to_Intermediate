# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import os.path
import random

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.text import slugify
from django.conf import settings
from blog.models import Post, Comment


def populate_database():
    password = 'dlfkajsdkl'
    User.objects.create_superuser(username='admin', email='admin@example.com', password=password)
    User.objects.create_user(username='user_1', email='user_1@example.com', password=password)
    User.objects.create_user(username='user_2', email='user2@example.com', password=password)

    authors = User.objects.all()
    titles = [
                "How to create a website using Pelican and Netlify (January 2021)",
                "Django, Axios and CSRF token",
                "A tour on Python Packaging",
                "Leaving Webfaction",
                "How python's import machinery works",
                "Webfaction LetsEncrypt Django",
                "Django custom sitemap (updated 2018)",
                "Django admin template structure",
                "How kto create a website using Pelican and Netlify (January 2021)",
                "Djangsdo, Axios and CSRF token",
                "A tour sdfon Python Packaging",
                "Leaving Wedsfsabfaction",
                "How python's imsdfport machinery works",
                "Webfaction LetsEncsdfrypt Django",
                "Django custom sitemapsdf (updated 2018)",
                "Django admin template stsdfructure",
                "Django admin tejlkjlkjlmplate structure",
                "How kto create a wej ljlk jklj bsite using Pelican and Netlify (January 2021)",
                "Djangsdo, Axios alk  lk kjnd CSRF token",
                "A tour sdfon Pyth jkl on Packaging",
                "Leaving Wedsfsab lkjlk faction",
                "How python's imsljl kldfport machinery works",
                "Webfaction LetsEnc lkj sdfrypt Django",
                "Django custom sitelj lk mapsdf (updated 2018)",
                "Django admin temp lkj late stsdfructure",
                "Django custom s;ljk itemapsdf (updated 2018)",
                "Django admin te  mplate stsdfructure",
                "Django admin te lk jlkjlkjlmplate structure",
                "How kto create klj a wej ljlk jklj bsite using Pelican and Netlify (January 2021)",
                "Djangsdo, Axio lk s alk  lk kjnd CSRF token",
                "A tour s lk dfon Pyth jkl on Packaging",
                "Leaving  lk Wedsfsab lkjlk faction",
                "How pyth lk on's imsljl kldfport machinery works",
                "Webfact klj ion LetsEnc lkj sdfrypt Django",
                "Django cu lk stom sitelj lk mapsdf (updated 2018)",
                "Django adlk min temp lkj late stsdfructure",
                "Djangsdo, Axio lk s alk  lk kjndjkl  CSRF token",
                "A tour s lk dfon Pyth jkl on Packlj kaging",
                "Leaving  lk Wedsfsab lkjlk fackl tion",
                "How pyth lk on's imsljl kldfporlk t machinery works",
                "Webfact klj ion LetsEnc lkj sdfrkj ypt Django",
                "Django cu lk stom sitelj lk maps klj df (updated 2018)",
                "Django adlk min temp lkj late stklj sdfructure",
            ]

    with open(os.path.join(settings.BASE_DIR, 'docs', 'Summary_Notes',
                           '007.Advance_Template.md')) as f:
        content = f.read()

    cnt = len(content)
    post_cnt = len(titles)
    bodies = []
    # chunks, chuck_size = cnt, int(cnt/post_cnt)
    # bodies = [content[i:i+chuck_size] for i in range(1, chunks, chuck_size)]
    for i in range(0, post_cnt):
        start = random.randint(30, cnt-2600)  # starting point
        length = random.randint(400, 2500)  # length of each post
        bodies.append(content[start:start+length])

    status = ['draft', 'published']

    for k in range(0, post_cnt):
        Post.objects.create(title=titles[k], body=bodies[k],
                            slug=slugify(titles[k]),
                            author=random.choice(authors),
                            status=random.choice(status))

    tags = [
        "technology", "india", "bhfyp", "business", "marketing", "gaming",
        "apple", "digital", "education", "samsung", "startup", "future",
        "technology", "techno", "science", "tech", "covid", "android",
        "engineering", "mobile", "innovation",
    ]
    posts = Post.objects.all()
    for i in range(0, len(posts)):
        tag_cnt = random.randint(2, 5)
        for e in random.sample(tags, tag_cnt):
            posts[i].tags.add(e)
        posts[i].save()

    posts = Post.published.all()
    names = [
        "Liam", "Olivia", "Noah", "Emma", "Oliver", "Charlotte", "Elijah", "Amelia", "James", "Ava",
        "William", "Sophia", "Benjamin", "Isabella", "Lucas", "Mia", "Henry", "Evelyn", "Theodore",
        "Harper",
    ]
    emails = [
        "Liam@example.com",  "Olivia@example.com",  "Noah@example.com",  "Emma@example.com",
        "Oliver@example.com",  "Charlotte@example.com",  "Elijah@example.com",  "Amelia@example.com",
        "James@example.com",  "Ava@example.com", "William@example.com",  "Sophia@example.com",
        "Benjamin@example.com",  "Isabella@example.com",  "Lucas@example.com",
        "Mia@example.com",  "Henry@example.com",  "Evelyn@example.com",  "Theodore@example.com",
        "Harper@example.com",
    ]

    bodies.clear()

    cnt = len(content)
    comment_cnt = len(posts) * 400
    # chunks, chuck_size = cnt, int(cnt/post_cnt)
    # bodies = [content[i:i+chuck_size] for i in range(1, chunks, chuck_size)]

    for i in range(1, comment_cnt):
        start = random.randint(30, cnt-600)  # starting point
        length = random.randint(100, 500)  # length of each post
        bodies.append(content[start:start+length])

    for k in range(0, len(posts)*4):
        Comment.objects.create(post=random.choice(posts), name=random.choice(names),
                               email=random.choice(emails), body=random.choice(bodies))

    site = Site()
    site.domain = 'localhost:8000'
    site.save()
