from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list(request):
    """
    Essa funcao exibe uma lista de posts marcados
    como publicados e ordenados pela data da publicacao.

    **Context**

    ``post``
       Uma instancia :model:`blog.Post`.

    **Template:**

    :template:`blog/post_list.html`
    """
    
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
    return render(request,'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    """
    Essa funcao exibe os detalhes de um post

    **Context**

    ``post``
       Uma instancia :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """
    post = get_object_or_404(Post, pk=pk)
    return render(request,'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    """
    Essa funcao registra o conteúdo de um novo post

    **Context**

    ``post``
       Uma instancia :model:`blog.Post`.

    ``form``

    **Template:**

    :template:`blog/post_detail.html`
    """
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request,'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    """
    Essa funcao registra e atualiza as modificações do conteudo de um post existente

    **Context**

    ``post``
       Uma instancia :model:`blog.Post`.

    **Template:**

    :template:`blog/post_edit.html`
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    """
    Essa funcao exibe uma lista de posts não publicados/ sem data de publicacao

    **Context**

    ``post``
       Uma instancia :model:`blog.Post`.

    ``form``

    **Template:**

    :template:`blog/post_detail.html`
    """
    posts = Post.objects.filter(publish_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

