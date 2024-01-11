import os
from django.core.files import File
from django.utils import timezone
from django.urls import reverse

from django.utils.html import mark_safe
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField

from blog.utils import generate_audio, send_push_notification

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
LANGUAGE_CODE_MAPPING = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'zh-CN': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'ko': 'Korean',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'fi': 'Finnish',
    'no': 'Norwegian',
    'da': 'Danish',
    'pl': 'Polish',
    'vi': 'Vietnamese',
    'th': 'Thai',
    'id': 'Indonesian',
    'ms': 'Malay',
    'he': 'Hebrew',
    'el': 'Greek',
    'cs': 'Czech',
    'hu': 'Hungarian',
    'ro': 'Romanian',
    'bg': 'Bulgarian',
    'uk': 'Ukrainian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'hr': 'Croatian',
    'sr': 'Serbian',
    'mk': 'Macedonian',
    'sq': 'Albanian',
    'et': 'Estonian',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'hy': 'Armenian',
    'ka': 'Georgian',
    'uz': 'Uzbek',
    'kk': 'Kazakh',
    'ky': 'Kyrgyz',
    'tg': 'Tajik',
    'tk': 'Turkmen',
    'mn': 'Mongolian',
    'ps': 'Pashto',
    'fa': 'Persian',
    'ur': 'Urdu',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'gu': 'Gujarati',
    'or': 'Odia',
    'mr': 'Marathi',
    'ne': 'Nepali',
    'si': 'Sinhala',
    'ml': 'Malayalam',
    'kn': 'Kannada',
    'ta': 'Tamil',
    'te': 'Telugu',
    'am': 'Amharic',
    'sw': 'Swahili',
    'yo': 'Yoruba',
    'ha': 'Hausa',
    'ig': 'Igbo',
    'zu': 'Zulu',
    'xh': 'Xhosa',
    'af': 'Afrikaans',
    'is': 'Icelandic',
    'ga': 'Irish',
    'mt': 'Maltese',
    'th': 'Thai',
    'km': 'Khmer',
    'lo': 'Lao',
    'my': 'Burmese',
    'dz': 'Dzongkha',
    'yi': 'Yiddish',
    'jw': 'Javanese',
    'su': 'Sundanese',
    'ms': 'Malay',
    'fil': 'Filipino',
    'ceb': 'Cebuano',
    'hmn': 'Hmong',
    'haw': 'Hawaiian',
    'sm': 'Samoan',
    'to': 'Tongan',
    'mi': 'Maori',
    'fj': 'Fijian',
}

GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
LANG_CHOICES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('ru', 'Russian'),
    ('ja', 'Japanese'),
    ('zh-CN', 'Chinese (Simplified)'),
    ('ar', 'Arabic'),
    ('hi', 'Hindi'),
    ('ko', 'Korean'),
    ('tr', 'Turkish'),
    ('nl', 'Dutch'),
    ('sv', 'Swedish'),
    ('fi', 'Finnish'),
    ('no', 'Norwegian'),
    ('da', 'Danish'),
    ('pl', 'Polish'),
    ('vi', 'Vietnamese'),
    ('th', 'Thai'),
    ('id', 'Indonesian'),
    ('ms', 'Malay'),
    ('he', 'Hebrew'),
    ('el', 'Greek'),
    ('cs', 'Czech'),
    ('hu', 'Hungarian'),
    ('ro', 'Romanian'),
    ('bg', 'Bulgarian'),
    ('uk', 'Ukrainian'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('hr', 'Croatian'),
    ('sr', 'Serbian'),
    ('mk', 'Macedonian'),
    ('sq', 'Albanian'),
    ('et', 'Estonian'),
    ('lv', 'Latvian'),
    ('lt', 'Lithuanian'),
    ('hy', 'Armenian'),
    ('ka', 'Georgian'),
    ('uz', 'Uzbek'),
    ('kk', 'Kazakh'),
    ('ky', 'Kyrgyz'),
    ('tg', 'Tajik'),
    ('tk', 'Turkmen'),
    ('mn', 'Mongolian'),
    ('ps', 'Pashto'),
    ('fa', 'Persian'),
    ('ur', 'Urdu'),
    ('bn', 'Bengali'),
    ('pa', 'Punjabi'),
    ('gu', 'Gujarati'),
    ('or', 'Odia'),
    ('mr', 'Marathi'),
    ('ne', 'Nepali'),
    ('si', 'Sinhala'),
    ('ml', 'Malayalam'),
    ('kn', 'Kannada'),
    ('ta', 'Tamil'),
    ('te', 'Telugu'),
    ('ur', 'Urdu'),
    ('am', 'Amharic'),
    ('sw', 'Swahili'),
    ('yo', 'Yoruba'),
    ('ha', 'Hausa'),
    ('ig', 'Igbo'),
    ('zu', 'Zulu'),
    ('xh', 'Xhosa'),
    ('af', 'Afrikaans'),
    ('is', 'Icelandic'),
    ('ga', 'Irish'),
    ('mt', 'Maltese'),
    ('th', 'Thai'),
    ('km', 'Khmer'),
    ('lo', 'Lao'),
    ('my', 'Burmese'),
    ('si', 'Sinhala'),
    ('ka', 'Georgian'),
    ('mn', 'Mongolian'),
    ('dz', 'Dzongkha'),
    ('yi', 'Yiddish'),
    ('jw', 'Javanese'),
    ('su', 'Sundanese'),
    ('ms', 'Malay'),
    ('fil', 'Filipino'),
    ('ceb', 'Cebuano'),
    ('hmn', 'Hmong'),
    ('haw', 'Hawaiian'),
    ('sm', 'Samoan'),
    ('to', 'Tongan'),
    ('mi', 'Maori'),
    ('fj', 'Fijian'),
)

COUNTRY_CHOICES = sorted(COUNTRY_CHOICES, key=lambda x: x[1])
class Language(models.Model):
    name = models.CharField(max_length=100, choices=LANG_CHOICES)
    code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return LANGUAGE_CODE_MAPPING.get(self.code,'')

    def save(self, *args, **kwargs):
        self.code = self.name  # Assign the name to the code field
        send_push_notification(title="Language", body="Language Created", data={"key": "value"})
        super().save(*args, **kwargs)
        
       

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
    preferred_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
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
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # send_push_notification(title="user created", body="user Created", data={"key": "value"})


class Category(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=120,default="Hii this is the discription")
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_push_notification(title="Category", body="Category Created", data={"key": "value"})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True,null=True)
    description = models.TextField(max_length=120,default="Hii this is the discription")
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_push_notification(title="Tag", body="Tag Created", data={"key": "value"})
   
    
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    post_cat = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    tags = models.ManyToManyField(Tag)
    post_slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None,always_update=True )  
    title = models.CharField(max_length=200)
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    published_date = models.DateTimeField(blank=True, null=True,default=timezone.now)
    image = models.ImageField(null=True,blank=True,upload_to='')
    feature_img = models.ImageField(null=True,blank=True,upload_to='blog_images')
    audio_file = models.FileField( null=True, blank=True)
    
    def save(self, *args, **kwargs):
        is_new_post = not bool(self.pk)
        audio_file_path = os.path.join('media', 'audio', f'{self.post_slug}.mp3')
        generate_audio(self.text, audio_file_path)

        with open(audio_file_path, 'rb') as file:
            self.audio_file.save(os.path.basename(audio_file_path), File(file), save=False)
        if is_new_post:
            send_push_notification(title="Created", body="New post Created", data={"key": "value"})
        else:
            send_push_notification(title="Updated", body="Post Updated", data={"key": "value"})
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        send_push_notification(title="Deleted", body="Post Deleted", data={"key": "value"})
        super().delete(*args, **kwargs)
        
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
    

class HashTag(models.Model):
    title = models.CharField(max_length=50,unique=True,null=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_push_notification(title="Hash tags created", body="hash tag created", data={"key": "value"})
    
    
class HashTagPost(models.Model):
    title = models.CharField(max_length=50, unique=True,null=True)
    content = models.TextField(null=True)
    hashtagsm2m = models.ManyToManyField(HashTag,blank=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        is_new_post = not bool(self.pk)
        super().save(*args, **kwargs)
        if is_new_post:
            send_push_notification(title="Created", body="New post Created", data={"key": "value"})
        else:
            send_push_notification(title="Updated", body="Post Updated", data={"key": "value"})
    def delete(self, *args, **kwargs):
        send_push_notification(title="Deleted", body="Post Deleted", data={"key": "value"})
        super().delete(*args, **kwargs)
    
    
@receiver(m2m_changed, sender=HashTagPost.hashtagsm2m.through)
def handle_hashtags_m2m_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        m2m_changed.disconnect(handle_hashtags_m2m_change, sender=HashTagPost.hashtagsm2m.through)
        for hashtag_id in pk_set:
            hashtag = HashTag.objects.get(pk=hashtag_id)
            instance.hashtagsm2m.add(hashtag)

        m2m_changed.connect(handle_hashtags_m2m_change, sender=HashTagPost.hashtagsm2m.through)

@receiver(post_save, sender=HashTagPost)
def extract_and_save(sender, instance, **kwargs):
    post_save.disconnect(extract_and_save, sender=HashTagPost)
    hashtags = [word[1:] for word in instance.content.split() if word.startswith('#')]
    # instance.hashtagsm2m.clear()
    for hashtag_title in hashtags:
        hashtag, created = HashTag.objects.get_or_create(title=hashtag_title)
        instance.hashtagsm2m.add(hashtag)
    instance.save()
    post_save.connect(extract_and_save, sender=HashTagPost)
    

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
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_push_notification(title="commented", body="comment Created", data={"key": "value"})
    
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)


    
