from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Count
from taggit.models import Tag
from blog.models import Post
from blog.forms import EmailPostForm, CommentForm, SearchForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

PER_PAGE = 5


# Function view
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    # filter the list of posts by the ones that contain the given tag, if any
    # since this is a many-to-many relationship, you have to filter posts by
    # tags contained in a given list,
    # many-to-many relationships occur when multiple objects of a model are associate with multiple
    # objects of another model.
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, per_page=PER_PAGE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {
                    'posts': posts,
                    'page_obj': posts,
                    'tag': tag
                })


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, slug=post_slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )

    # list of active comments for this post
    #
    # recall the following line in blog/models.py
    #
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    #
    # instead of building a QuerySet for the Comment model directly,
    # you leverage the post object to retrieve the related Comment Objects.
    # you use the manager for the related objects that you defined as comments using
    # the related_name attribute of the relationship in the Comment model.
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()

    # List of similar posts
    # retrieve a Python list of IDs for the tags of the current post
    # the values_list() returns tuples with the values for the given fields.
    # flat=True to get single values such as [1, 2, 3, ...] instead of one-tuples such as [(1, ), (2, ), ...]
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts,
                   })


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@example.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results = Post.published.annotate(search=SearchVector('title', 'body')).filter()
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector,
                                              rank=SearchRank(search_vector, search_query)
                                              ).filter(search=search_query).order_by('-rank')

    return render(request, 'blog/post/search.html', {'form': form,
                                                     'query': query,
                                                     'results': results})


# Class-based View
class PostListView(ListView):
    # use a specific QuerySet instead of retrieving all objects
    queryset = Post.published.all()
    # instead of defining a `queryset` attribute, you could have specified
    # model = Post, and Django would have built the generic Post.objects.all()
    # querySet for you
    # model = Post
    #

    # use the 'posts' context variable for the query results,
    # the default variable is `object_list`, if you don't specify any
    # context_object_name
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    template_name = 'blog/post/list.html'
