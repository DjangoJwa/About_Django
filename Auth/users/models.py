from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, username, name, email=None, password=None, **extra_fields):
        """
        일반 사용자 생성 메서드
        """
        try:
            user = self.model(
                username=username,
                name=name,
                email=email if email else "",
            )
            extra_fields.setdefault('is_staff', False)
            extra_fields.setdefault('is_superuser', False)
            user.set_password(password)
            user.is_active = True
            user.save()
            return user
        except ValidationError:
            raise ValidationError({'detail': 'Enter a name proper'})

    def create_superuser(self, username, name, email=None, password=None, **extra_fields):
        """
        관리자 생성 메서드
        """
        try:
            superuser = self.create_user(
                username=username,
                name=name,
                password=password
            )
            superuser.is_admin = True
            superuser.is_superuser = True
            superuser.is_active = True
            superuser.save()
            return superuser
        except:
            raise ValidationError({'detail': 'Enter a proper email account'})


# 전체 서비스의 커스텀 유저 모델
class User(AbstractBaseUser, PermissionsMixin):
    # 회원 가입시 입력받는 유저 ID
    username = models.CharField(max_length=30, unique=True)

    # 회원 가입시 입력받는 유저 이름
    name = models.CharField(max_length=30)

    # 회원 가입시 입력받는 유저 이메일
    email = models.EmailField(default='')

    # AbstractBaseUser 상속 받음으로써 정의해줘야 하는 Bool 필드
    is_staff = models.BooleanField(default=False)
    if_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # custom manager 설정
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.name if self.name else self.username

    @property
    def is_staff(self):
        """일반 사용자 or 스태프 권한"""
        return self.is_admin
    
    def has_module_perms(self, app_label):
        """user가 주어진 app_label에 해당 권한이 있는지 확인"""
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_module_perms(self, app_label)
    
    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_module_perms(self, perm, obj)

    # AbstractBaseUser에는 존재하지 않으므로 따로 선언
    def user_permission(self):
        return self._user_permissions
    
    # 장고 admin 이름 출력시 필요한 메소드
    def get_full_name():
        return self.username
    
    def get_short_name():
        return self.username