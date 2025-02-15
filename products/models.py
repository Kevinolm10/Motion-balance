from django.db import models
import cloudinary.models
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
        'self', on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    nav_element = models.CharField(
        max_length=20,
        choices=PARENT_CATEGORY,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

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


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sizes = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text="Comma-separated list of sizes (e.g., S,M,L,XL)")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    discount_percentage = models.FloatField(
        null=True,
        blank=True)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    subcategory_name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True)

    # Parent category choices
    parent_category = models.CharField(
        max_length=20,
        choices=[
            ('products', 'Products'),
            ('accessories', 'Accessories'),
            ('sale', 'Sale'),
        ],
        default='products'
    )

    tags = models.ManyToManyField(Tag, related_name='products', blank=True)
    average_rating = models.FloatField(default=0.0)

    @property
    def discounted_price(self):
        if self.discount_percentage:
            discount_decimal = Decimal(
                str(self.discount_percentage)) / Decimal('100')
            Decimal
            return self.price * (Decimal('1') - discount_decimal)
        return self.price  # If no discount, return original price

    def save(self, *args, **kwargs):
        """Link product to subcategory
        under the selected parent category and calculate discount price."""
        if not self.subcategory_name:
            raise ValidationError("Subcategory name is required.")

        # Find the parent category based on the parent_category field value
        parent_category = Category.objects.filter(
            nav_element=self.parent_category, parent__isnull=True).first()
        if not parent_category:
            raise ValidationError(
                f"Parent category '{self.parent_category}' does not exist.")

        # Create or get the subcategory based on the subcategory_name
        subcategory, created = Category.objects.get_or_create(
            name=self.subcategory_name,
            parent=parent_category,
            defaults={'slug': self.subcategory_name.lower().replace(" ", "-")}
        )
        self.category = subcategory

        # Validate size only if the product is not an accessory
        if self.parent_category != 'accessories' and not self.sizes:
            raise ValidationError("Sizes are required for this product.")

        if self.discount_percentage is not None:
            discount_decimal = Decimal(
                str(self.discount_percentage)) / Decimal('100')
            self.discount_price = self.price * (
                Decimal('1') - discount_decimal)

        super().save(*args, **kwargs)

    def update_average_rating(self):
        """Recalculate the average rating when a new review is added."""
        avg_rating = self.feedback.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = round(avg_rating, 2) if avg_rating else 0.0
        self.save()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images')
    image = cloudinary.models.CloudinaryField('image')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductFeedback(models.Model):
    STARS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=STARS)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_item = models.ForeignKey(
        'checkout.OrderItem', on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                'user', 'product'], name='unique_user_product_feedback')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_average_rating()

    def __str__(self):
        return f"Feedback from {self.user.username} for {self.product.name}"
