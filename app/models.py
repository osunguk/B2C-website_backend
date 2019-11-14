from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    BUSINESS = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (BUSINESS, 'Business'),
        (CUSTOMER, 'Customer')
    )
    NOMAL = 1
    KAKAO = 2
    FACEBOOK = 3
    NAVER = 4
    USER_TYPE = (
        (NOMAL, 'Nomal'),
        (KAKAO, 'Kakao'),
        (FACEBOOK, 'Facebook'),
        (NAVER, 'Naver')
    )
    # 기본 정보
    role_profile = models.PositiveSmallIntegerField('BC 유형', choices=ROLE_CHOICES, null=True, blank=True)
    user_type = models.PositiveSmallIntegerField('사용자 유형', choices=USER_TYPE, null=True, blank=True, default=1)

    def __str__(self):  # u_id .=. username
        return str(self.username)


class Store(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    store_name = models.CharField('가게 이름', max_length=30)
    business_number = models.IntegerField('사업자 번호')
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="store-image/%Y/%m/%d")

    def __str__(self):
        return str(self.store_name)


class Store_file(models.Model):
    s_id = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.s_id)


class Review(models.Model):
    s_id = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, related_name="Store")
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    star_score = models.IntegerField('별점', default=1, validators=[MinValueValidator(1),
                                                                   MaxValueValidator(5)])

    def __str__(self):
        return str(self.s_id)


class Review_file(models.Model):
    r_id = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    # filename = models.CharField(max_length=100, null=True)
    # original_name = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.r_id)


class Review_comment(models.Model):
    s_id = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    r_id = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # owner
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.r_id)


class HashTag(models.Model):
    tag_title = models.CharField(max_length=30)

    def __str__(self):
        return str(self.tag_title)


class StoreTags(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    s_id = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    t_id = models.ForeignKey(HashTag, on_delete=models.CASCADE, null=True)


