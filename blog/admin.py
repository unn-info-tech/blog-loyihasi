from django.contrib import admin
from .models import Like, Post, Izoh, PostRasm, Profil

from django.contrib import admin
from django.db.models import Count
from .models import Post, Profil

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('sarlavha', 'muallif', 'yaratilgan_sana', 'nashr_etilgan', 'korildi')
    list_filter = ('nashr_etilgan', 'yaratilgan_sana', 'muallif')
    search_fields = ('sarlavha', 'matn')
    date_hierarchy = 'yaratilgan_sana'
    ordering = ('-yaratilgan_sana',)

    # Filtrlar
    list_per_page = 20

    # Fieldsets (guruhlar)
    fieldsets = (
        ('Asosiy Malumotlar', {
            'fields': ('sarlavha', 'matn', 'muallif')
        }),
        ('Qoshimcha', {
            'fields': ('rasm', 'nashr_etilgan'),
            'classes': ('collapse',)
        }),
        ('Statistika', {
            'fields': ('korildi', 'yaratilgan_sana', 'yangilangan_sana'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('yaratilgan_sana', 'yangilangan_sana', 'korildi')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('muallif')

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('foydalanuvchi', 'manzil', 'tugilgan_sana')
    search_fields = ('foydalanuvchi__username', 'bio')
    list_filter = ('tugilgan_sana',)

@admin.register(Izoh)
class IzohAdmin(admin.ModelAdmin):
    list_display = ('post', 'muallif', 'yaratilgan')
    list_filter = ('yaratilgan',)
    search_fields = ('matn',)




@admin.register(PostRasm)
class PostRasmAdmin(admin.ModelAdmin):
    list_display = ('post', 'rasm')



@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    list_filter = ('user', 'post')