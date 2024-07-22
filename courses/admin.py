from django.contrib import admin
from .models import Chapter,Course,Matter,Media,Evaluation,Question,Tutorial,Challenge,Transaction

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Media)
admin.site.register(Matter)
admin.site.register(Evaluation)
admin.site.register(Question)
admin.site.register(Tutorial)
admin.site.register(Challenge)
admin.site.register(Transaction)