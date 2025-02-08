from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Avg
from decimal import Decimal

# Category Model
class Category(models.Model):
    PARENT_CATEGORY = [
        ('products', 'Products'),
        ('accessories', 'Accessories'),
        ('sale', 'Sale'),
    ]

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )
    nav_element = models.CharField(
        max_length=20,
        choices=PARENT_CATEGORY,
        default='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

# Category Manager
    @classmethod
    def create_parent_categories(cls):
        """Create top-level parent categories if they don't exist."""
        for category in cls.PARENT_CATEGORY:
            name = category[1]
            slug = category[0]
            cls.objects.get_or_create(name=name, slug=slug, parent=None)

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.FloatField(null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    subcategory_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    parent_category = models.CharField(max_length=20, choices=Category.PARENT_CATEGORY, default='products')
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)
    average_rating = models.FloatField(default=0.0)  # Store instead of calculating dynamically

    def save(self, *args, **kwargs):
        """Link product to subcategory under the selected parent category and calculate discount price."""
        if not self.subcategory_name:
            raise ValidationError("Subcategory name is required.")

        parent_category = Category.objects.filter(nav_element=self.parent_category, parent__isnull=True).first()
        if not parent_category:
            raise ValidationError(f"Parent category '{self.parent_category}' does not exist.")

        subcategory, created = Category.objects.get_or_create(
            name=self.subcategory_name,
            parent=parent_category,
            defaults={'slug': self.subcategory_name.lower().replace(" ", "-")}
        )
        self.category = subcategory

        if self.discount_percentage is not None:
            discount_decimal = Decimal(str(self.discount_percentage)) / Decimal('100')
            self.discount_price = self.price * (Decimal('1') - discount_decimal)

        super().save(*args, **kwargs)

    def update_average_rating(self):
        """Recalculate the average rating when a new review is added."""
        avg_rating = self.productfeedback_set.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = round(avg_rating, 2) if avg_rating else 0.0
        self.save()

    def __str__(self):
        return self.name

# Product Variant Model
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=50, null=True, blank=True)  # Example: S, M, L
    color = models.CharField(max_length=50, null=True, blank=True)  # Example: Red, Blue
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"

# Product Image Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/')
    alt_text = models.CharField(max_length=255, blank=True)  # SEO-friendly

    def __str__(self):
        return f"Image for {self.product.name}"

# Product Feedback Model
class ProductFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order_item = models.ForeignKey('checkout.OrderItem', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_average_rating()

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.product.name}"
