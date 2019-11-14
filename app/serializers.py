from django.contrib.auth.models import Group
from django.db.models import Avg
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from rest_framework import serializers


from .models import User, Store, Review, Review_comment, \
    Review_file, Store_file, HashTag, StoreTags


class MyRegistrationSerializer(RegisterSerializer):
    Business = serializers.BooleanField(required=False)
    user_type = serializers.CharField(required=False, max_length=30)

    def custom_signup(self, request, user):
        print('check')
        _user_type = self.validated_data.get('user_type')
        u = User.objects.get(username=user.username)
        if _user_type == 'kakao':
            u.user_type = 2
        elif _user_type == 'facebook':
            u.user_type = 3
        elif _user_type == 'naver':
            u.user_type = 4
        else:
            u.user_type = 1
        if self.validated_data.get('Business'):
            u.role_profile = 1
            u.is_staff = True
            u.save()
        else:
            u.role_profile = 2
            u.save()


class MyRegistrationView(RegisterView):
    serializer_class = MyRegistrationSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class StoreSerializer(serializers.ModelSerializer):
    current_user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())  # 현재접속유저
    reviews_count = serializers.SerializerMethodField('review_count_f')         # 댓글 갯수
    average_star_score = serializers.SerializerMethodField('aver_star_score')   # 평균 평점

    def review_count_f(self, obj):
        reviews = Review.objects.filter(s_id=obj)
        return reviews.count()

    def aver_star_score(self, obj):
        average = Review.objects.filter(s_id=obj).aggregate(Avg('star_score'))
        return average['star_score__avg']

    class Meta:
        model = Store
        fields = ('url', 'id', 'u_id', 'store_name',
                  'business_number', 'title', 'content', 'image',
                  'current_user', 'reviews_count', 'average_star_score'
                  )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('url', 'id', 's_id', 'u_id',
                  'comment', 'created_at', 'star_score',
                  )


class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review_comment
        fields = ('url', 'id', 's_id', 'r_id', 'u_id',
                  'comment', 'created_at'
                  )


class ReviewFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review_file
        fields = ('id', 'r_id', 'image'
                  )


class StoreFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store_file
        fields = ('id', 's_id', 'image'
                  )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('url', 'id', 'tag_title',)


class StoreTagSerializer(serializers.ModelSerializer):
    get_tag_title = serializers.SerializerMethodField('get_tag_title_f')

    def get_tag_title_f(self, obj):
        tag_title = HashTag.objects.get(id=obj.t_id.id)
        return tag_title.tag_title

    class Meta:
        model = StoreTags
        fields = ('s_id', 't_id', 'u_id', 'get_tag_title')
