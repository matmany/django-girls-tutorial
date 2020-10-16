from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
    return render(request,'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request,'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
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
    posts = Post.objects.filter(publish_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    """
    Redireciona ao `post_detail`, Após a publicação.

    Para publicar é necessario estar logado. 
    Umas vez publicado é redirecionado ao `blog/post_detail.html`

    **Context**

    ``pk``
        Uma Key de :model:`blog.Post`.
    
    **Templates:**

    :template:`blog/post_detail.html`
    """
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    """
   Deleta um Post e Redireciona ao `post_detail`. 

   Delete o Post selecionado pela `pk`.
    **Templates:**

    :template:`blog/post_list.html`
    """
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    """
    Exibe formulario do `blog.forms.CommentForm` ou Redireciona ao `post_detail`.

    O formulario blog/add_comment_to_post.html é exibido. \n 
    Caso haja um requisito POST, o formulario é validado e salvo.
    
    **Context**

    ``form``
        Uma instancia `blog.forms.CommentForm`

    ``pk``
        Uma Key de :model:`blog.Post`.
    
    **Templates:**

    :template:`blog/add_comment_to_post.html`

    :template:`blog/post_detail.html`
    """
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
    """
    Exibe Detalhes de um :model:`blog.Post` quando comentario é removido.

    **Context**

    ``pk``
        Uma Key de :model:`blog.Post`.
    
    **Template:**

    :template:`blog/post_detail.html`
    """
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def comment_approve(request, pk):
    """
    Redireciona para `post_detail` quando comentario é aprovado

    **Context**

    ``pk``
        Uma Key de :model:`blog.Post`.
    
    **Template:**

    :template:`blog/post_detail.html`
    """
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)