from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Avg


# Create your models here.



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

    @classmethod
    def create_parent_categories(cls):
        """Create top-level parent categories if they don't exist."""
        for category in cls.PARENT_CATEGORY:
            name = category[1]
            slug = category[0]
            cls.objects.get_or_create(name=name, slug=slug, parent=None)




class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.FloatField(null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_image = models.ImageField(upload_to='products/')

    subcategory_name = models.CharField(max_length=255)  # Subcategory name
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='products', null=True, blank=True
    )
    parent_category = models.CharField(
        max_length=20,
        choices=Category.PARENT_CATEGORY,
        default='products'
    )

    def save(self, *args, **kwargs):
        """Link product to subcategory under the selected parent category."""
        if not self.subcategory_name:
            raise ValidationError("Subcategory name is required.")

        # Ensure the parent category exists
        parent_category = Category.objects.filter(nav_element=self.parent_category, parent__isnull=True).first()

        if not parent_category:
            raise ValidationError(f"Parent category '{self.parent_category}' does not exist.")

        # Get or create the subcategory under the parent category
        subcategory, created = Category.objects.get_or_create(
            name=self.subcategory_name,
            parent=parent_category,
            defaults={'slug': self.subcategory_name.lower().replace(" ", "-")}
        )

        # Assign the subcategory to the product
        self.category = subcategory

        # Calculate discount price if applicable
        if self.discount_percentage is not None:
            discount_decimal = Decimal(str(self.discount_percentage)) / Decimal('100')
            self.discount_price = self.price * (Decimal('1') - discount_decimal)

        super().save(*args, **kwargs)

    def average_rating(self):
        """Calculate the average rating of the product."""
        avg_rating = self.productfeedback_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 2) if avg_rating else None

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def calculate_total_price(self):
        self.total_price = sum(item.total_price for item in self.order_items.all())
        self.save()


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem {self.id} - {self.product.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ProductFeedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Feedback {self.feedback_id} - {self.product.name}"


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist {self.id} - {self.product.name}"