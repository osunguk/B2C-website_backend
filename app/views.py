import requests
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.response import Response

from .helpers import modify_input_for_multiple_files, store_modify_input_for_multiple_files
from . import models
from . import serializers
from .permissions import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.http import JsonResponse


class UserList(generics.ListCreateAPIView):
    permission_classes = []
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class TagList(generics.ListCreateAPIView):
    queryset = models.HashTag.objects.all()
    serializer_class = serializers.TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.HashTag.objects.all()
    serializer_class = serializers.TagSerializer


class MyStoreTag(generics.ListAPIView):
    queryset = models.StoreTags.objects.all()
    serializer_class = serializers.StoreTagSerializer
    lookup_url_kwarg = 's_id'

    def get_queryset(self):
        s_id = self.kwargs.get(self.lookup_url_kwarg)
        tag = models.StoreTags.objects.filter(s_id=s_id)
        return tag


class TaggingStore(generics.ListAPIView):
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        t_id = self.kwargs.get(self.lookup_url_kwarg)
        tag = models.StoreTags.objects.filter(t_id=t_id)
        store_list =[]
        for t in tag:
            s = models.Store.objects.get(store_name=t.s_id)
            store_list.append(s)
        return store_list


class StoreTagList(generics.ListCreateAPIView):
    queryset = models.StoreTags.objects.all()
    serializer_class = serializers.StoreTagSerializer


class CurrentUser(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(username=self.request.user)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class StoreList(generics.ListCreateAPIView):  # 전체 가게리스트
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer


class StoreDetail(generics.RetrieveUpdateDestroyAPIView):  # 가게 정보 수정
    permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer


class MyStoreDetail(generics.ListCreateAPIView):  # 자신의 가게만 보여줌
    permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer

    def get_queryset(self):
        return super().get_queryset().filter(u_id=self.request.user)


class ReviewList(generics.ListCreateAPIView):  # 댓글 리스트
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def create(self, request, *args, **kwargs):
        request.data['u_id'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StoreReviewList(generics.ListAPIView):  # 해당가게 댓글 리스트
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    lookup_url_kwarg = 's_id'

    def get_queryset(self):
        s_id = self.kwargs.get(self.lookup_url_kwarg)  # api 요청시 value 값 받음 - /review/store/<value>
        review = models.Review.objects.filter(s_id=s_id)
        return review


class StoreReviewCommentList(generics.ListAPIView):  # 해당가게 대댓글 리스트
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    lookup_url_kwarg = 's_id'

    def get_queryset(self):
        s_id = self.kwargs.get(self.lookup_url_kwarg)  # api 요청시 value 값 받음 - /review/store/<value>
        review_comment = models.Review_comment.objects.filter(s_id=s_id)
        return review_comment


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):  # 댓글 수정
    permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class ReviewComment(generics.ListCreateAPIView):  # 사장님 답글
    permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Review_comment.objects.all()
    serializer_class = serializers.ReviewCommentSerializer

    def create(self, request, *args, **kwargs):
        request.data['u_id'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Review_comment.objects.all()
    serializer_class = serializers.ReviewCommentSerializer


class ReviewFile(generics.ListCreateAPIView):
    queryset = models.Review_file.objects.all()
    serializer_class = serializers.ReviewFileSerializer


class ReviewFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review_file.objects.all()
    serializer_class = serializers.ReviewFileSerializer


class StoreFile(generics.ListCreateAPIView):
    queryset = models.Store_file.objects.all()
    serializer_class = serializers.ReviewFileSerializer


class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        all_images = models.Review_file.objects.all()
        serializer = serializers.ReviewFileSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        #filename = request.data['filename']
        #original_name = request.data['original_name']
        r_id = request.data['r_id']
        # converts querydict to original dict
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(r_id, img_name)
            file_serializer = serializers.ReviewFileSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class StoreImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        all_images = models.Store_file.objects.all()
        serializer = serializers.StoreFileSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        #filename = request.data['filename']
        #original_name = request.data['original_name']
        s_id = request.data['s_id']
        # converts querydict to original dict
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = store_modify_input_for_multiple_files(s_id, img_name)
            file_serializer = serializers.StoreFileSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class MyStoreImage(generics.ListAPIView):  # 해당가게 이미지 리스트
    queryset = models.Store_file.objects.all()
    serializer_class = serializers.StoreFileSerializer
    lookup_url_kwarg = 's_id'

    def get_queryset(self):
        s_id = self.kwargs.get(self.lookup_url_kwarg)  # api 요청시 value 값 받음 - /review/store/<value>
        images = models.Store_file.objects.filter(s_id=s_id)
        return images


class MyStoreImageDetail(generics.RetrieveUpdateDestroyAPIView):  # 해당가게 이미지디테일
    queryset = models.Store_file.objects.all()
    serializer_class = serializers.StoreFileSerializer


class MyReviewImage(generics.ListAPIView):  # 해당 리뷰 리스트
    queryset = models.Review_file.objects.all()
    serializer_class = serializers.ReviewFileSerializer
    lookup_url_kwarg = 'r_id'

    def get_queryset(self):
        r_id = self.kwargs.get(self.lookup_url_kwarg)  # api 요청시 value 값 받음 - /review/store/<value>
        images = models.Review_file.objects.filter(r_id=r_id)
        return images

def oauth(request):
    # # 사용자 요청->카카오api->code발급
    # code = request.GET.get('code')
    # client_id = '63e4734e72d2d421ef9d5ff9200a241f'
    # redirect_uri = 'http://127.0.0.1:8000/oauth/'
    #
    # print('code : ', code)
    #
    # # 발급받은 code를 통해 access token 발급
    # data = {
    #     'grant_type': 'authorization_code',
    #     'client_id': client_id,
    #     'redirect_uri': redirect_uri,
    #     'code': code
    # }
    # response = requests.post('https://kauth.kakao.com/oauth/token', data=data)
    # response_json = response.json()
    # print('json', response_json)
    #
    # # access token을 이용하여 사용자 정보받기
    # headers = {
    #     'Authorization': 'Bearer {}'.format(response_json['access_token']),
    # }
    # response2 = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
    # response2_json = response2.json()
    #
    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    # print(response2_json)
    # nickName = str(response2_json['properties']['nickname']) + str('#' + str(response2_json['id']))
    # if not models.User.objects.filter(username=nickName):
    #     models.User.objects.create_user(nickName)
    # # u = AbstractUser(username=str(response2_json['properties']['nickname']) + str('#' + str(response2_json['id'])))
    # # u.set_password('')
    # # u.is_staff = False
    # # u.save()
    print(request)
    return redirect(to='http://localhost:3000/main')