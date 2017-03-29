from django.db import models

class Question(models.Model):
    question_text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text
