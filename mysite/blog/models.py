from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    """
    Armazena um unico Post, se relaciona com
    :model: `auth.User`. 

    Para publicar o Post é preciso executar a função publish()
    
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Nome ou Pseudónimo do Usuario")
    title = models.CharField(help_text="Titulo do Post",max_length=200)
    text = models.TextField(help_text="Texto do Post")
    created_date = models.DateTimeField(help_text="Data de criação do Post",default=timezone.now)
    publish_date = models.DateTimeField(help_text="Data de publicação do Post",blank = True, null = True)

    def publish(self):
        """Publica o post. Atribuindo a hora e data atual ao `publish_date`.
        """
        self.publish_date = timezone.now()
        self.save()
    
    def __str__(self):
        """Retorna o title do Post

        Returns
        -------
        CharField
            O titulo do Post
        """
        return self.title

    def approved_comments(self):
        """Retorna lista de comentarios aprovados pelo administrador"""
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    """
    Armazena um unico comentario, se relaciona com
    :model: `blog.Post`. 

    O comentario precisa de aprovação do administrador
    para servisualizado.
    """
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(help_text="Nome ou Pseudónimo do autor",max_length=200)
    text = models.TextField(help_text="Texto do Comentario")
    created_date = models.DateTimeField(help_text="Data de criação do Comentario",default=timezone.now)
    approved_comment = models.BooleanField(help_text="Estado de aprovação do comentario",default=False)

    def approve(self):
        """Realiza aprovação do Comment. Atribuindo `True` ao `approved_comment`
        e salva."""
        self.approved_comment = True
        self.save()
    
    def __str__(self):
        """Retorna o texto do Comment

        Returns
        -------
        TextField
            O texto do Comment
        """
        return self.text