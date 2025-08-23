from rest_framework import viewsets, permissions
from .models import Asset
from .serializers import AssetSerializer

class AssetViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Asset.objects.all()
        return Asset.objects.filter(added_by=user)
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            from rest_framework.response import Response
            from rest_framework import status
            return Response({'error': 'Only superusers can edit assets.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            from rest_framework.response import Response
            from rest_framework import status
            return Response({'error': 'Only superusers can edit assets.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)
