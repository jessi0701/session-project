from django.contrib import admin
from .models import Movie,Score
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class MovieResource(resources.ModelResource):
    class Meta:
        model = Movie
# Register your models here.
class MovieAdmin(ImportExportModelAdmin):
    resource_class = MovieResource

admin.site.register(Movie, MovieAdmin)
admin.site.register(Score)