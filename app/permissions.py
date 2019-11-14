from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용하므로,
        # GET, HEAD, OPTIONS 요청은 항상 허용함
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_superuser:
            return True

        # 쓰기 권한은 가게 등록 및 댓글 생성한 사람만 가능
        return obj.u_id == request.user
