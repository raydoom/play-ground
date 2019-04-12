

from rest_framework import serializers, viewsets

from app.models import UserInfo

# Serializers define the API representation.
class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('id', 'user_id', 'username', 'email', "is_superuser")


# ViewSets define the view behavior.
class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer