import csv
from django.core.management.base import BaseCommand
from map.models import location

class Command(BaseCommand):
    help = 'import cities from a csv'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='path to the csv file')
        
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        created_count = 0
        
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    city, created = location.objects.get_or_create(
                        city=row['city'],
                        state=row['state'],
                        defaults={
                            'latitude': float(row['latitude']),
                            'longitude': float(row['longitude']),
                        }
                    )
                    
                    if created:
                        created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Made {created_count} cities!"))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found"))
        except Exception as e:
            self.stdout.write(self.style.SUCCESS(f"Error {e} occured"))
            
            
                