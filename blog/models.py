from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone



    
class Category(models.Model):
    # post = models.ForeignKey(Post,on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True,null=True)
    def __str__(self):
        return self.name
    
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    published_date = models.DateTimeField(blank=True, null=True)
    blog_img = models.ImageField(null=True,blank=True,upload_to='blog_images/',)
    post_slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None, )  
    post_cat = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    tags = models.ManyToManyField(Tag)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
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
    COUNTRY_CHOICES = sorted(COUNTRY_CHOICES, key=lambda x: x[1])

    # Add more countries as needed
    gender = models.CharField(max_length=60,null=True,choices=GENDER_CHOICES,blank=True)
    phone = models.PositiveBigIntegerField(null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    img = models.ImageField(null=True,blank=True,upload_to='profile_images/',)
    designation = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField(max_length=50,null=True,blank=True)
    pincode = models.PositiveIntegerField(null=True,blank=True)
    city = models.CharField(max_length=80,null=True,blank=True)
    state = models.CharField(max_length=90,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True,choices=COUNTRY_CHOICES)
    def __str__(self):
        return self.username

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self) :
        return self.text

class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return self.text