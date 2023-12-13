from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from django.utils.html import mark_safe
from django.urls import reverse


COUNTRY_CHOICES = [
    ('CN', 'China'),
    ('IN', 'India'),
    ('US', 'United States'),
    ('ID', 'Indonesia'),
    ('PK', 'Pakistan'),
    ('BR', 'Brazil'),
    ('NG', 'Nigeria'),
    ('BD', 'Bangladesh'),
    ('RU', 'Russia'),
    ('MX', 'Mexico'),
    ('JP', 'Japan'),
    ('ET', 'Ethiopia'),
    ('PH', 'Philippines'),
    ('EG', 'Egypt'),
    ('VN', 'Vietnam'),
    ('CD', 'Democratic Republic of the Congo'),
    ('TR', 'Turkey'),
    ('IR', 'Iran'),
    ('DE', 'Germany'),
    ('TH', 'Thailand'),
    ('GB', 'United Kingdom'),
    ('FR', 'France'),
    ('IT', 'Italy'),
    ('TZ', 'Tanzania'),
    ('ZA', 'South Africa'),
    ('KR', 'South Korea'),
    ('CO', 'Colombia'),
    ('KE', 'Kenya'),
    ('AR', 'Argentina'),
    ('UA', 'Ukraine'),
    ('SD', 'Sudan'),
    ('PL', 'Poland'),
    ('DZ', 'Algeria'),
    ('CA', 'Canada'),
    ('UG', 'Uganda'),
    ('MA', 'Morocco'),
    ('PE', 'Peru'),
    ('IQ', 'Iraq'),
    ('SA', 'Saudi Arabia'),
    ('UZ', 'Uzbekistan'),
    ('MY', 'Malaysia'),
    ('VE', 'Venezuela'),
    ('AF', 'Afghanistan'),
    ('GH', 'Ghana'),
    ('NP', 'Nepal'),
    ('YE', 'Yemen'),
    ('KP', 'North Korea'),
    ('MG', 'Madagascar'),
    ('CM', 'Cameroon'),
    ('CI', 'Ivory Coast'),
    ('AU', 'Australia'),
    ('NE', 'Niger'),
    ('TW', 'Taiwan'),
    ('LK', 'Sri Lanka'),
    ('BF', 'Burkina Faso'),
    ('ML', 'Mali'),
    ('RO', 'Romania'),
    ('MW', 'Malawi'),
    ('CL', 'Chile'),
    ('KZ', 'Kazakhstan'),
    ('ZM', 'Zambia'),
    ('GT', 'Guatemala'),
    ('EC', 'Ecuador'),
    ('SY', 'Syria'),
    ('NL', 'Netherlands'),
    ('SN', 'Senegal'),
    ('KP', 'Cambodia'),
    ('TD', 'Chad'),
    ('SO', 'Somalia'),
    ('ZW', 'Zimbabwe'),
    ('RW', 'Rwanda'),
    ('GN', 'Guinea'),
    ('BJ', 'Benin'),
    ('TN', 'Tunisia'),
    ('BE', 'Belgium'),
    ('CU', 'Cuba'),
    ('BO', 'Bolivia'),
    ('HT', 'Haiti'),
    ('GR', 'Greece'),
    ('DO', 'Dominican Republic'),
    ('CZ', 'Czech Republic'),
    ('PT', 'Portugal'),
    ('SV', 'El Salvador'),
    ('HN', 'Honduras'),
    ]

GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
   
COUNTRY_CHOICES = sorted(COUNTRY_CHOICES, key=lambda x: x[1])

# Custom user modal using AbstractUser and added some new fields
class CustomUser(AbstractUser):
    gender = models.CharField(max_length=60,choices=GENDER_CHOICES,blank=True)
    city = models.CharField(max_length=80,blank=True)
    state = models.CharField(max_length=90,blank=True)
    country = models.CharField(max_length=50,blank=True,default='IN',choices=COUNTRY_CHOICES)
    designation = models.CharField(max_length=50,null=True,blank=True)
    img = models.ImageField(blank=True,null=True,upload_to='profile_images/',default='default_img.jpg')
    phone = models.PositiveBigIntegerField(blank=True,default=0000000)
    pincode = models.PositiveIntegerField(blank=True,null=True)
    address = models.TextField(max_length=50,blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    
    def __str__(self):
        return self.username
    
    def img_preview(self): 
        return mark_safe('<img src = "{url}" width = "25"/>'.format(
             url = self.img.url 
         ))
        
    def img_preview2(self): 
        return mark_safe('<img src = "{url}" width = "100"/>'.format(
             url = self.img.url
         ))


class Category(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=120,default="Hii this is the discription")
    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True,null=True)
    description = models.TextField(max_length=120,default="Hii this is the discription")
    def __str__(self):
        return self.name
   
    
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_cat = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    tags = models.ManyToManyField(Tag)
    post_slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None,always_update=True )  
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(null=True,blank=True)
    feature_img = models.ImageField(null=True,blank=True)
    def img_preview(self): 
        return mark_safe('<img src = "{url}" width = "25"/>'.format(
             url = self.image.url
         ))
        
    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_slug': self.post_slug})
    
    def __str__(self):
        return self.title
    
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)
    

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(null=True)
    name = models.CharField(max_length=50)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    class Meta:
        ordering = ('-created',)
        
    def __str__(self) :
        return self.name
    
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

