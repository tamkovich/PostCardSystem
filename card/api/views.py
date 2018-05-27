from django.db.models import Q
from rest_framework import generics, mixins
from card.models import UserCard
from .serializers import UserCardSerializer
# from .permissions import IsOwnerOrReadOnly


class UserCardAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = UserCardSerializer
    # permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = UserCard.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(city__icontains=query)|Q(transport__icontains=query)).distinct()
        return qs

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class UserCardRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = UserCardSerializer

    def get_queryset(self):
        return UserCard.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
