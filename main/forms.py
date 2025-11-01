from django import forms
from main.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "category", "price", "stock",
            "color", "size", "thumbnail",
            "description", "promo",
            "is_featured" 
        ]
        labels = {
            "promo": "Promo Product",
            "thumbnail": "Thumbnail (Image URL)"
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": 'Masukkan nama produk, contoh: "Adidas Predator 2025"',
                "class": "w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-green-500 focus:border-green-500"
            }),
            "thumbnail": forms.URLInput(attrs={
                "placeholder": "contoh: https://example.com/image.jpg",
                "class": "w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-green-500 focus:border-green-500"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Tuliskan deskripsi produk kamu di sini...",
                "class": "w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-green-500 focus:border-green-500"
            }),
            "promo": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
            }),
        }

    price = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "placeholder": "contoh: 299900",
            "class": "w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-green-500 focus:border-green-500"
        })
    )

    stock = forms.IntegerField(
        min_value=5, max_value=100,
        widget=forms.NumberInput(attrs={
            "placeholder": "Minimal 5, maksimal 100",
            "class": "w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-green-500 focus:border-green-500"
        })
    )

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
        common_attrs = {
            'class': 'w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-green-500 focus:border-green-500',
        }
        
        self.fields['category'].widget = forms.TextInput(attrs={
            **common_attrs, 'placeholder': 'Pilih atau ketik kategori baru', 'list': 'category-datalist'
        })
        self.fields['color'].widget = forms.TextInput(attrs={
            **common_attrs, 'placeholder': 'Pilih atau ketik warna baru', 'list': 'color-datalist'
        })
        self.fields['size'].widget = forms.TextInput(attrs={
            **common_attrs, 'placeholder': 'Pilih atau ketik ukuran baru', 'list': 'size-datalist'
        })

        self.fields['category'].widget.datalist_id = 'category-datalist'
        self.fields['category'].widget.datalist = list(Product.objects.values_list('category', flat=True).distinct().order_by('category'))
        
        self.fields['color'].widget.datalist_id = 'color-datalist'
        self.fields['color'].widget.datalist = list(Product.objects.values_list('color', flat=True).distinct().order_by('color'))

        self.fields['size'].widget.datalist_id = 'size-datalist'
        self.fields['size'].widget.datalist = list(Product.objects.values_list('size', flat=True).distinct().order_by('size'))