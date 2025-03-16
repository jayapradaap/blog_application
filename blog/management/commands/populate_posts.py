from typing import Any
from blog.models import Post,Category
from django.core.management.base import BaseCommand
import random



class Command(BaseCommand):
    help = "This command is for inserting the post data"


    def handle(self, *args, **options):
        
        #Deleting th existing data
        Post.objects.all().delete()
        titles = ["Flight",
          "Cars",
          "Bikes",
          "Formula1",
          "Isle of man TT",]
        contents = ["The flight was invented by Wright Brothers and now it is one of the largest and one of the easiest way of transportation",
                "Cars with gasoline engines going to disappear in the near future and will be replaced by more efficiet and pollutionless electric motors",
                "Bikes are more crazy and intresting to ride and day by day the bike enthusiasm is growing all around the world",
                "Formula1 2026 going to have a new car with new regulations and seems will be more intreesting",
                "Isle of man TT is one of the most dangerous and thrilling bike race in the world",
                ]
        image_urls = ["https://picsum.photos/id/364/800/400",
                    "https://picsum.photos/id/133/800/400",
                    "https://picsum.photos/id/428/800/400",
                    "https://picsum.photos/id/744/800/400",
                    "https://picsum.photos/id/563/800/400",
                    ]

        categories = Category.objects.all()
        for title,content,image_url in zip(titles,contents,image_urls):
            category = random.choice(categories)
            Post.objects.create(title=title,content=content,image_url=image_url,category=category)
        
        self.stdout.write(self.style.SUCCESS("Completed insertung the data!"))
