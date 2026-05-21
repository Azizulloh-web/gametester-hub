from rest_framework import generics
from .models import Game
from .serializers import GameSerializer

class GameListAPI(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameDetailAPI(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer