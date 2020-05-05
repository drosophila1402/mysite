from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User, PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator

from django import forms
from django.conf import settings
# from stdimage.models import StdImageField
from adminsortable.models import SortableMixin


class Category(SortableMixin):
    name = models.CharField(max_length=225, verbose_name='カテゴリ')
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    
    class Meta:
        ordering = ['the_order']
        verbose_name_plural = '商品カテゴリ'
    
    def __str__(self):
        return self.name
 
      
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='商品名')
    image = models.ImageField(upload_to='images', default='defo', verbose_name='商品画像')
    brand = models.CharField(max_length=255, verbose_name='ブランド')
    material = models.CharField(max_length=255, verbose_name='素材')
    pick_up = models.BooleanField('ピックアップ', default=False, help_text='ピックアップ欄に追加する場合はチェックを入れてください')
    description = models.TextField(verbose_name='商品説明')
    price = models.IntegerField(default=0, verbose_name='価格')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='カテゴリ')
    quantity = models.IntegerField(default=0, verbose_name='数量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日')


    class Meta:
        verbose_name_plural = '商品'
        
    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def __str__(self):
        return self.name
        

"""書かないとcreatesuperuserできない"""
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

"""お気に入り機能追加済みユーザー"""
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)

    favorite_products = models.ManyToManyField(Product, verbose_name='お気に入り商品', blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class InfoCategory(SortableMixin):
    name = models.CharField(max_length=225, verbose_name='カテゴリ名')
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    
    class Meta:
        ordering = ['the_order']
        verbose_name_plural = 'インフォカテゴリ'
    
    def __str__(self):
        return self.name
        
    
class Info(models.Model):
    title = models.CharField(max_length=255, verbose_name='タイトル')
    text = models.TextField(verbose_name='本文')
    category = models.ManyToManyField(InfoCategory, verbose_name='カテゴリ', blank=True)
    published_at = models.DateTimeField(default=timezone.now, verbose_name='公開日時')
    is_public = models.BooleanField('公開する', default=False, help_text='公開する場合はチェックを入れてください')
    
    
    class Meta:
        verbose_name_plural = 'インフォ'
    
    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name='氏名')
    email = models.EmailField(verbose_name='メールアドレス')
    subject = models.CharField(max_length=255, verbose_name='件名')
    text = models.TextField(verbose_name='本文')

    class Meta:
        verbose_name_plural = '問い合わせ'
    
    def __str__(self):
        return self.subject

class Comment(models.Model):
    author = models.CharField(max_length=255, verbose_name='投稿者')
    text = models.TextField(verbose_name='本文')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='投稿日')
    post = models.ForeignKey('ec.Info', on_delete=models.CASCADE, related_name='comments', verbose_name='投稿')
    approve = models.BooleanField('表示する', default=True, help_text='非公開にする場合はチェックを外してください')
    

        
    class Meta:
        verbose_name_plural = 'コメント'
    
    def __str__(self):
        return self.author
