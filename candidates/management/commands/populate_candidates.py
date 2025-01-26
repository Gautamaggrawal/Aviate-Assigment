from django.core.management.base import BaseCommand
from candidates.models import Candidate
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate dynamic test candidate data'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, 
                             help='Number of candidates to generate')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()
        
        # Clear existing data
        Candidate.objects.all().delete()

        # Generate candidates
        candidates = []
        for _ in range(count):
            gender = random.choice(['M', 'F', 'O'])
            
            # Generate name with higher chance of multiple word names
            name_formats = [
                fake.first_name(), 
                f"{fake.first_name()} {fake.last_name()}",
                f"{fake.first_name()} {fake.last_name()} {fake.last_name()}"
            ]
            name = random.choice(name_formats)

            candidate = Candidate(
                name=name,
                age=random.randint(22, 55),
                gender=gender,
                email=fake.unique.email(),
                phone_number=fake.numerify(text='##########')
            )
            candidates.append(candidate)

        # Bulk create for efficiency
        Candidate.objects.bulk_create(candidates)

        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} test candidates'))