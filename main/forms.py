from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'color', 'size', 'thumbnail', 'description', 'is_featured']
