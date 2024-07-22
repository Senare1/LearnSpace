from django.db import models
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import mimetypes
from django.utils.text import slugify
from accounts.constants import TEACHER_MATTER, DIFFICULTY, LEARNER_LEVEL, FIRST_CYCLE, choix

class Matter(models.Model):
    matter_name = models.CharField(max_length=32, unique=True, choices=TEACHER_MATTER, default="math")
    is_first_cycle = models.BooleanField(default=True)

    def __str__(self):
        return self.matter_name

class Evaluation(models.Model):
    evaluation_name = models.CharField(max_length=32)
    evaluation_matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name="evaluations")

    def __str__(self):
        return self.evaluation_name

class Transaction(models.Model):
    learner = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, blank=True, null=True, related_name="transactions")
    transId = models.CharField(max_length=200, null=True)
    token = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=128)

    def __str__(self):
        return str(self.id)

@deconstructible
class FileValidator:
    def __init__(self, allowed_types, message=None):
        self.allowed_types = allowed_types
        self.message = message or 'Type de fichier non autorisé.'

    def __call__(self, value):
        mime_type, encoding = mimetypes.guess_type(value.name)
        if mime_type not in self.allowed_types:
            raise ValidationError(self.message)

validate_image = FileValidator(
    allowed_types=[
        'image/jpeg', 'image/png', 'image/gif', 'image/webp'
    ],
    message='Seules les images sont autorisées.'
)

validate_video = FileValidator(
    allowed_types=[
        'video/mp4', 'video/avi', 'video/mpeg', 'video/webm', 'video/mkv'
    ],
    message='Seules les vidéos sont autorisées.'
)

validate_audio = FileValidator(
    allowed_types=[
        'audio/mpeg', 'audio/mp3', 'audio/ogg', 'audio/wav', 'audio/x-wav'
    ],
    message='Seuls les fichiers audio sont autorisés.'
)

validate_document = FileValidator(
    allowed_types=[
        'application/pdf', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ],
    message='Seuls les documents sont autorisés.'
)

class Question(models.Model):
    question = models.TextField()
    response = models.TextField()
    question_evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="questions")
    
    def save(self, *args, **kwargs):
        self.question = self.question.lower()
        self.response = self.response.lower()
        super().save(*args, **kwargs)

class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True, verbose_name="Code du cours")
    course_title = models.CharField(max_length=128, verbose_name="Titre du cours")
    slug = models.SlugField(unique=True, blank=True, null=True)
    text_content = models.TextField(blank=True, null=True, verbose_name="Contenu en texte")
    course_level = models.CharField(max_length=128, choices=LEARNER_LEVEL, default="SIXIEME")
    course_matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name='courses', verbose_name="Matiere")
    course_author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="courses")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    difficulty = models.CharField(max_length=32, choices=DIFFICULTY, verbose_name="Difficulté du cours")
    is_premium = models.BooleanField(default=False, verbose_name="Status du cours")

    def save(self, *args, **kwargs):
        if not self.slug or (self.course_title != self.slug.split('-')[0] or self.course_code != self.slug.split('-')[1]):
            self.slug = slugify(f"{self.course_title}-{self.course_code}")
            if Course.objects.filter(slug=self.slug).exists():
                num = 1
                while Course.objects.filter(slug=f"{self.slug}-{num}").exists():
                    num += 1
                self.slug = f"{self.slug}-{num}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_title

class Chapter(models.Model):
    chapter_title = models.CharField(max_length=32, unique=True)
    content_text = models.TextField(blank=True, null=True)
    chapter_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    
    def __str__(self):
        return self.chapter_title

class Media(models.Model):
    image_media = models.ImageField(upload_to='courses/images/', validators=[validate_image], blank=True, null=True)
    video_media = models.FileField(upload_to='courses/videos/', validators=[validate_video], blank=True, null=True)
    audio_media = models.FileField(upload_to='courses/audio/', validators=[validate_audio], blank=True, null=True)
    document_media = models.FileField(upload_to='courses/documents/', validators=[validate_document], blank=True, null=True)
    media_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='medias')

    def __str__(self):
        return self.image_media.name if self.image_media else (
            self.video_media.name if self.video_media else (
                self.audio_media.name if self.audio_media else (
                    self.document_media.name if self.document_media else 'No File'
                )
            )
        )

class Tutorial(models.Model):
    tutorial_name = models.CharField(max_length=128)
    tutorial_matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name="tutorials")
    tutorial_videos = models.FileField(upload_to='courses/videos/', validators=[validate_video], blank=True, null=True)

    def __str__(self):
        return self.tutorial_name

class Challenge(models.Model):
    challenge_name = models.CharField(max_length=128)
    challenge_matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name="challenges")
    challenge_image = models.FileField(upload_to='courses/images/', validators=[validate_image], blank=True, null=True)
    challenge_document = models.FileField(upload_to='courses/documents/', validators=[validate_document], blank=True, null=True)

    def __str__(self):
        return self.challenge_name
