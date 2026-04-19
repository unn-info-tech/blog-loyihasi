from rest_framework import serializers
from .models import Post, Profil
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Izoh
from .models import Profil


class PostSerializer(serializers.ModelSerializer):
    muallif_ismi = serializers.CharField(source='muallif.username', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'sarlavha',
            'matn',
            'muallif',
            'muallif_ismi',
            'rasm',
            'yaratilgan_sana',
            'yangilangan_sana',
            'nashr_etilgan',
            'korildi'
        ]
        read_only_fields = ['id', 'yaratilgan_sana', 'yangilangan_sana', 'korildi', 'muallif']




class IzohSerializer(serializers.ModelSerializer):
    class Meta:
        model = Izoh
        fields = '__all__'




class ProfilSerializer(serializers.ModelSerializer):
    foydalanuvchi_ismi = serializers.CharField(source='foydalanuvchi.username', read_only=True)

    class Meta:
        model = Profil
        fields = '__all__'


class PostBatafsilSerializer(serializers.ModelSerializer):
    izohlar = IzohSerializer(source='izoh_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'