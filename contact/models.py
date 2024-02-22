from django.db import models


class Contact(models.Model):
    """
    Represents a contact message.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} | {self.subject}"