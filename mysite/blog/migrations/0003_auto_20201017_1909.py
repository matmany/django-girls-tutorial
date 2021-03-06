# Generated by Django 2.2.16 on 2020-10-17 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='avatar_url',
            field=models.TextField(blank=True, help_text='URL da img', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='img_url',
            field=models.TextField(blank=True, help_text='URL da img', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='approved_comment',
            field=models.BooleanField(default=False, help_text='Estado de aprovação do comentario'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(help_text='Nome ou Pseudónimo do autor', max_length=200),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Data de criação do Comentario'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Texto do Comentario'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(help_text='Nome ou Pseudónimo do Usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Data de criação do Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(blank=True, help_text='Data de publicação do Post', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(help_text='Texto do Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Titulo do Post', max_length=200),
        ),
    ]
