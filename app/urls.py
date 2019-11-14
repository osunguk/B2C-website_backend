from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .serializers import MyRegistrationView
from . import views

urlpatterns = [
    path('rest-auth/registration/signup/', MyRegistrationView.as_view()),
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('current-user/', views.CurrentUser.as_view(), name='current-user'),

    path('store/', views.StoreList.as_view()),
    path('store/<int:pk>', views.StoreDetail.as_view(), name='store-detail'),
    path('mystore/', views.MyStoreDetail.as_view()),

    path('review/', views.ReviewList.as_view()),
    path('review/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),
    path('review-comment/', views.ReviewComment.as_view()),
    path('review-comment/<int:pk>', views.ReviewCommentDetail.as_view(), name='review_comment-detail'),

    path('review/store/<int:s_id>', views.StoreReviewList.as_view()),  # 해당가게의 댓글
    path('review-comment/store/<int:s_id>', views.StoreReviewCommentList.as_view()),  # 해당가게의 대댓글
    path('mystore-file/<int:s_id>', views.MyStoreImage.as_view()),   # 해당 가게 사진 GET
    path('myreview-file/<int:r_id>', views.MyReviewImage.as_view()),  # 해당 가게 리뷰 사진 GET
    path('mystore-file/<int:s_id>/<int:pk>', views.MyStoreImageDetail.as_view()),
    path('review-file/', views.ReviewFile.as_view()),
    path('review-file/<int:pk>', views.ReviewFileDetail.as_view(), name='review_file-detail'),
    path('review-files/', views.ImageView.as_view()),
    path('store-file/', views.StoreImageView.as_view()),

    path('oauth/', views.oauth),

    path('tag/', views.TagList.as_view()),
    path('tag/<int:pk>', views.TagDetail.as_view(), name='hashtag-detail'),
    path('tagging-store/<int:pk>', views.TaggingStore.as_view()),
    path('mystore-tag/<int:s_id>', views.MyStoreTag.as_view()),
    path('StoreTags/',views.StoreTagList.as_view()),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
