# Generated by Django 2.0.2 on 2020-05-05 06:58

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ec.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', ec.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('the_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'verbose_name_plural': '商品カテゴリ',
                'ordering': ['the_order'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approve', models.BooleanField(default=False, verbose_name='非表示にする')),
            ],
            options={
                'verbose_name_plural': 'コメント',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
            options={
                'verbose_name_plural': '問い合わせ',
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('text', models.TextField(verbose_name='本文')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='公開日時')),
                ('is_public', models.BooleanField(default=False, help_text='公開する場合はチェックを入れてください', verbose_name='公開する')),
            ],
            options={
                'verbose_name_plural': 'インフォ',
            },
        ),
        migrations.CreateModel(
            name='InfoCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('the_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'verbose_name_plural': 'インフォカテゴリ',
                'ordering': ['the_order'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('text', models.TextField(verbose_name='本文')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='公開日時')),
                ('is_public', models.BooleanField(default=False, help_text='公開する場合はチェックを入れてください', verbose_name='公開する')),
            ],
            options={
                'verbose_name_plural': 'ニュース',
            },
        ),
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('the_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'verbose_name_plural': 'ニュースカテゴリ',
                'ordering': ['the_order'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(default='defo', upload_to='images')),
                ('brand', models.CharField(max_length=255)),
                ('material', models.CharField(max_length=255)),
                ('pick_up', models.BooleanField(default=False, help_text='ピックアップ欄に追加する場合はチェックを入れてください', verbose_name='ピックアップ')),
                ('description', models.TextField()),
                ('price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ec.Category')),
            ],
            options={
                'verbose_name_plural': '商品',
            },
        ),
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.ManyToManyField(blank=True, to='ec.NewsCategory', verbose_name='カテゴリ'),
        ),
        migrations.AddField(
            model_name='info',
            name='category',
            field=models.ManyToManyField(blank=True, to='ec.InfoCategory', verbose_name='カテゴリ'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ec.News'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='favorite_products',
            field=models.ManyToManyField(blank=True, to='ec.Product', verbose_name='お気に入り商品'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
