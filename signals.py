"""
1.Django signals are executed synchronously. This means that when a signal is sent, 
the connected signal handlers (functions) execute immediately, blocking the main thread 
until they complete."""
import time
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print(f"Signal received for instance: {instance.name}")
    start_time = datetime.datetime.now()
    
    time.sleep(3) 

    end_time = datetime.datetime.now()
    print(f"Signal processing done. Time taken: {end_time - start_time}")

if __name__ == "__main__":
    start = datetime.datetime.now()
    
    obj = MyModel(name="Test Instance")
    obj.save()  

    end = datetime.datetime.now()
    
    print(f"Total execution time: {end - start}")


"""
2. Django signals run in the same thread as the caller by default. 
They are synchronous unless explicitly configured to run asynchronously 
"""
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, **kwargs):
    print(f"Signal running in thread: {threading.get_ident()}")


def create_user():
    print(f"Caller running in thread: {threading.get_ident()}")
    user = User.objects.create(username="testuser")

create_user()

"""
3.Yes, by default, Django signals run in the same database transaction as the caller.
 This means that if an exception occurs in a signal handler and is not caught, 
 it can cause the entire transaction to be rolled back. Conversely, if the caller's 
 transaction is rolled back, the changes made in the signal handler will also be undone.
"""
# models.py
from django.db import models
from django.db import transaction
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("Signal: Creating UserProfile")
        UserProfile.objects.create(user=instance)

# test_signals.py
from django.db import transaction
from django.contrib.auth.models import User
from app_name.models import UserProfile

try:
    with transaction.atomic():
        print("Creating user inside transaction...")
        user = User.objects.create(username="testuser")
        print("User created, but transaction not committed yet.")
        
        raise Exception("Something went wrong!")

except Exception as e:
    print(f"Exception occurred: {e}")

print("Checking if user exists:", User.objects.filter(username="testuser").exists())
print("Checking if user profile exists:", UserProfile.objects.filter(user__username="testuser").exists())


# CUSTOM CLASSES IN PYTHON

class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
        self._attributes = [{'length': self.length}, {'width': self.width}]
    
    def __iter__(self):
        return iter(self._attributes)

rect = Rectangle(5, 15)

for attr in rect:
    print(attr)
