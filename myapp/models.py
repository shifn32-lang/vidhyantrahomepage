from django.db import models


class ContactInquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False, help_text="Tick once you have replied to this inquiry.")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'contact inquiry'
        verbose_name_plural = 'contact inquiries'

    def __str__(self):
        return f'{self.name} - {self.service}'


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email
