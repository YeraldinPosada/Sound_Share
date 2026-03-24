from rest_framework import generics
from .models import Song
from .serializers import SongSerializer

# Crear canción
class SongCreateView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

# Obtener todas las canciones (con filtro por género)
class SongListView(generics.ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = Song.objects.all()
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)
        return queryset

# Obtener, actualizar o eliminar una canción
class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer