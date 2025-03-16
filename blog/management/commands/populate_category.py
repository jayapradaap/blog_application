from typing import Any
from blog.models import Category
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "This command is for inserting the post data"


    def handle(self, *args, **options):
        
      #Deleting th existing data
      Category.objects.all().delete
      categories = [
         "Inventions",
         "Innovations",
         "Hobbies",
         "Sports",
         
      ]

      for category_name in categories:
        Category.objects.create(name = category_name)
        
      self.stdout.write(self.style.SUCCESS("Completed insertung the data!"))
