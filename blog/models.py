from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    title=models.CharField(max_length=200)

    def __str__(self):
        return self.title
# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=220,unique=True,blank=True)
    content=models.TextField()
    author=models.CharField(max_length=100,default='anonymous')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    class Meta:
        ordering=['-created_at']
        indexes=[
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base=slugify(self.title)[:200]
            slug=base
            i=1
            while Post.objects.filter(slug=slug).exists():
                i+=1
                slug=f"{base}-{i}"
            self.slug=slug

        super().save(*args, **kwargs)






#ilk 17 deq sual cavab

#28 DEQ QAYDA

# Slug — saytın URL (link) hissəsində olan, oxunaqlı və sadə yazılış formasıdır.
#
# Məsələn, siz bir blog yazısı yazırsınız və başlıq belədir:
# "Django Framework ilə Veb Proqramlaşdırma"




# 📌 1. Clustered Index nədir?
#
# Verilənlərin özləri birbaşa indeksin içində saxlanılır.
#
# Yəni, verilənlər birbaşa sıralanmış şəkildə saxlanılır.
#
# Bir cədvəldə yalnız bir dənə clustered index ola bilər, çünki fiziki verilənlər ancaq bir qaydada sıralana bilər.
#
# 🔍 Nümunə:
#
# Tutaq ki, bir cədvəldə id sahəsi üzrə clustered index var. Bu zaman:
#
# id	ad	yaş
# 1	Ali	25
# 2	Vəli	30
# 3	Ayşe	28
#
# Verilənlər id-yə görə sıralanmış halda saxlanılır və bu sahəyə görə axtarış çox sürətlidir.


# ✔️ Clustered Index:
#
# Verilər birbaşa indeksin içində, fiziki olaraq sıralanmış şəkildə saxlanılır.
#
# Bu məlumatlar ağac strukturunda saxlanılır – əsasən B-tree (Balanced Tree) və ya B+ Tree.

# 📌 2. Non-clustered Index nədir?
#
# Verilənlərin özləri yox, sadəcə onların "ünvanı" (pointer) saxlanılır.
#
# Yəni, indeks ayrıca bir strukturda olur və orada:
#   - indekslənmiş sütunun dəyərləri
#   - həmin dəyərlərin yerləşdiyi sətirin ünvanı
# saxlanılır.
#
# Bir cədvəldə bir dənə clustered index ola bilər, amma çoxlu (10-larla) non-clustered index ola bilər.
#
# 🔍 Nümunə:
#
# id   ad    yaş
# 1    Ali   25
# 2    Vəli  30
# 3    Ayşe  28
#
# Cədvəl fiziki olaraq id-yə görə saxlanılır (clustered index).
# Amma ad sahəsi üzrə non-clustered index yaratsaq:
#
# Index (ad):
#   Ali  → id=1
#   Ayşe → id=3
#   Vəli → id=2
#
# İndi "Ayşe" axtarılanda:
#   1. Non-clustered index-də "Ayşe → id=3" tapılır
#   2. Sonra əsas cədvəldə id=3 olan sətir götürülür
#
# ✔️ Non-clustered Index:
#
# Verilənləri sıralamır, sadəcə ayrıca kataloq (mündəricat) yaradır.
# Bu da oxumağı sürətləndirir, amma əlavə "lookup" lazımdır.


#non clusterda axtaris oldugu zaman siralayir.yeni fiziki olaraq saxlayib ver clsuterd kimi




# Yox ❌ — bunların heç biri clustered index deyil.
#
# Django’dakı vəziyyət:
# indexes = [
#     models.Index(fields=['slug']),
#     models.Index(fields=['-created_at']),
# ]
#
#
# Bunlar sadəcə additional (əlavə) non-clustered index yaradır.
#
# Clustered index isə (demək olar ki, həmişə) sənin id sahəndir, çünki Django avtomatik PRIMARY KEY olaraq id yaradır, o da DB-də clustered olur.
#
# İzah:
#
# models.Index(fields=['slug'])
# → slug sütunu üçün non-clustered index.
#
# models.Index(fields=['-created_at'])
# → created_at sütunu üzrə descending non-clustered index.
#
# ➡️ İkisi də non-clustered.
# ➡️ Clustered yalnız primary key (id)-dir (əgər özün başqa sahəni primary_key=True etməmisənsə).
#
# 📌 Yəni:
#
# id = clustered index (default)
#
# slug, created_at = non-clustered indexlər (sən özün Meta.indexes ilə yaratmısan)

# Qısaca DB üçün belə deyə bilərsən:
#
# class Meta: → modelin verilənlər bazasında necə saxlanacağını idarə edir.
#
# Məsələn:
#
# db_table → cədvəlin adını təyin edir.
#
# ordering → default sıralamanı göstərir.
#
# unique_together / constraints → sahələr üzrə unikal qayda qoyur.
#
# 👉 Yəni Meta = modelin DB davranış qaydaları.

# Model.Meta → DB davranışı (cədvəl, sıralama, unikal qayda, indexlər).
#
# Form.Meta → Form davranışı (hansı sahələrdən form düzəlsin, hansı inputlarla göstərilsin).


# 🔹 *args
#
# “istənilən sayda əlavə arqument gələndə hamısını bir tuple-a yığ”.
#
# Yəni funksiyanı çağıranda neçə arqument gəlsə də qəbul edəcək.
#
# Misal:
#
# def test(*args):
#     print(args)
#
# test(1, 2, 3)
#
#
# çıxış:
#
# (1, 2, 3)
#
# 🔹 **kwargs
#
# “istənilən sayda açar=dəyər tipli arqument gələndə hamısını bir dict-ə yığ”.
#
# Misal:
#
# def test(**kwargs):
#     print(kwargs)
#
# test(name="Samir", age=25)
#
#
# çıxış:
#
# {'name': 'Samir', 'age': 25}
#
# 🔹 Birlikdə
# def test(*args, **kwargs):
#     print("args:", args)
#     print("kwargs:", kwargs)
#
# test(1, 2, 3, name="Samir", age=25)
#
#
# çıxış:
#
# args: (1, 2, 3)
# kwargs: {'name': 'Samir', 'age': 25}
#
# 🔹 Django-da niyə belə yazılır?
#
# Django-nun save() metodu çoxlu parametr qəbul edə bilər:
#
# force_insert=True
#
# force_update=True
#
# using="default"
#
# və s.
#
# Əgər biz save(self, *args, **kwargs) yazmasaq, bu əlavə parametrlər ötürülməzdi.
#
# ✅ Qısaca:
#
# *args → əlavə mövqeli arqumentlər.
#
# **kwargs → əlavə açar=dəyər arqumentləri.
#
# İkisi birlikdə → “nə gəlirsə qəbul elə, parent metoduna ötür”.
#
# İstəyirsən mən sənə Post.save()-də real nümunə göstərim: məsələn post.save(force_update=True) necə **kwargs ilə işləyir?


