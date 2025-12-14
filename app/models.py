from django.db import models

# Create your models here.
class Asset(models.Model):
    symbol = models.CharField(max_length=10, unique=True, help_text='Unique ticker symbol')
    name = models.CharField(max_length=100, help_text='Full name of the asset')
    is_active = models.BooleanField(default=True, help_text='If false, we stop fetching data for this asset')

    def __str__(self):
        return self.symbol


class PriceData(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=20, decimal_places=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['asset', '-timestamp']),]

    def __str__(self):
        return f'{self.asset.symbol} - {self.price} at {self.timestamp}'
