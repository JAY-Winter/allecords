from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="상품명")
    artist = models.CharField(max_length=200, verbose_name="아티스트명")
    url = models.URLField(max_length=500, verbose_name="상품 URL")
    image_url = models.URLField(max_length=500, verbose_name="이미지 URL")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="가격")

    class Meta:
        verbose_name = "제품"
        verbose_name_plural = "제품들"

    def __str__(self):
        return self.title
