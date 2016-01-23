from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm, ContactForm

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context

from likes.middleware import SecretBallotUserIpUseragentMiddleware

# Create your views here.

#######################################################################
#                     Clean Blog content                              #
#######################################################################

def blog_contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            contact_number = request.POST.get('contact_number', '')
            contact_message = request.POST.get('contact_message', '')

            # Email the profile with the 
            # contact information
            template = get_template('blog/contact_template.txt')
            context = Context({'contact_name': contact_name, 'contact_email': contact_email,'contact_number': contact_number, 'contact_message': contact_message,})
            content = template.render(context)
            #print content

            email = EmailMessage(
                "Message from MELAONGO",
                content,
                " melaongo " +'<melaongo.heroku.com>',
                ['srinaveen.desu@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('melaongo.views.blog_contact')
        
    return render(request, 'blog/blog_contact.html', {'form': form_class,})

def blog_about(request):
    #return render_to_response('blog/blog_about.html')
    return render(request, 'blog/blog_about.html')

##def blog(request):
##    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
##    return render(request, 'blog/blog.html', {'posts': posts})
##
##def blog_post_detail(request, pk):
##    post = get_object_or_404(Post, pk=pk)
##    return render(request, 'blog/post.html', {'post': post})


#######################################################################
#                    Normal Blog content                              #
#######################################################################


def post_list(request):
    posts_list = Post.objects.all().filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    paginator = Paginator(posts_list, 10)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    sbp = SecretBallotUserIpUseragentMiddleware()
    sbp.process_request(request)
        
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    sbp = SecretBallotUserIpUseragentMiddleware()
    sbp.process_request(request)
    
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_add.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('melaongo.views.post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('melaongo.views.post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('melaongo.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('melaongo.views.post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('melaongo.views.post_detail', pk=post_pk)
