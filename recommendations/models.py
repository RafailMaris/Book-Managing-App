from django.db import models

class BookSummary(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    summary = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("title", "author")

    def __str__(self):
        return f"{self.title} — {self.author}"

