from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class LikeMeUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, sex, birth_date, phone_number, password=None, is_active=True,
                    is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not password:
            raise ValueError("Users must have a password")
        if not sex:
            raise ValueError("Users must have a sex")
        if not birth_date:
            raise ValueError("Users must have a birth_date")
        if not phone_number:
            raise ValueError("Users must have a phone_number")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birth_date=birth_date,
            phone_number=phone_number
        )
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, sex, birth_date, phone_number, password=None):
        user = self.create_user(email, first_name=first_name, last_name=last_name, sex=sex, birth_date=birth_date,
                                phone_number=phone_number, password=password, is_staff=True)
        return user

    def create_superuser(self, email, first_name, last_name, sex, birth_date, phone_number, password):
        user = self.create_user(email, first_name=first_name, last_name=last_name, sex=sex, birth_date=birth_date,
                                phone_number=phone_number, password=password, is_staff=True, is_admin=True)
        return user


class LikeMeUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=90, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    sex = models.IntegerField(default=0)
    birth_date = models.DateTimeField(default=timezone.now)
    phone_number = models.TextField(default=0)
    photo = models.ImageField(upload_to='profiles/', default='profiles/profile_default.png')
    profile_state = models.IntegerField(default=0)

    join_date = models.DateTimeField(verbose_name='join date', auto_now_add=True)

    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser

    USERNAME_FIELD = 'email'
    # email and password are required by default
    REQUIRED_FIELDS = ['first_name', 'last_name', 'sex', 'birth_date', 'phone_number']

    objects = LikeMeUserManager()

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def __str__(self):
        return self.get_full_name()

    # =============

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


User = LikeMeUser


class FriendShip(models.Model):
    id = models.AutoField(primary_key=True)
    user_sender = models.ForeignKey(User, related_name="friendship_sender_set", on_delete=models.CASCADE)
    user_receiver = models.ForeignKey(User, related_name="friendship_receiver_set", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "FriendShip from " + str(self.user_sender) + " to " + str(self.user_receiver)


class Posteig(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200)
    user_post = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200)
    user_post = models.ForeignKey(User, on_delete=models.CASCADE)
    posteig_id = models.ForeignKey(Posteig, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200)
    user_post = models.ForeignKey(User, on_delete=models.CASCADE)
    posteig_id = models.ForeignKey(Comments, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Posteig, on_delete=models.CASCADE)
    user_like = models.ForeignKey(User, on_delete=models.CASCADE)
    like_type = models.CharField(max_length=200, default="1")

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Posteig, on_delete=models.CASCADE)
    user_report = models.ForeignKey(User, on_delete=models.CASCADE)
    report_message = models.CharField(max_length=200)
