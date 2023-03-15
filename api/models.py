from django.db import models
# sau khi tao modal chay python manage.py migrate
#sau do chay python manage.py makemigrations
# Create your models here.
class Account(models.Model):
    username = models.TextField(null=False, blank='')
    password = models.TextField(null=False, blank='')
    email = models.EmailField(null=False, blank='', default="")
    sdt = models.TextField(null=True, blank='')
    location = models.TextField(null=True, blank='')
    fullname = models.TextField(null=True, blank='')

    def __str__(self):
        return self.username

class Note(models.Model):
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    
class Collection(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.title

class Book(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(null=True, blank=True, upload_to="static/images/")
    description = models.CharField(max_length=1000)
    author = models.CharField(max_length=50)
    publishYear = models.IntegerField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null= False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return (self.user,"-",self.date_ordered,"-",self.complete)
    
    @property
    def get_cart_total(self):
        orderitems = self.item.all()
        total = sum([item.get_total_cost for item in orderitems])
        return total
    
class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null= False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null= False, related_name= 'item')
    date_add = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    @property
    def get_total_cost(self):
        total = self.book.price * self.quantity
        return total
