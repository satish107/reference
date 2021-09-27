from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline

b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
b.save() # Now it will hit database on save() method call

# Saving Foreign Key
entry = Entry.objects.get(pk=1)
cheese_blog = Blog.objects.get(name="Cheddar Talk")
entry.blog = cheese_blog
entry.save()

# Saving ManyToMany Fields
joe = Author.objects.create(name="Joe")
entry.authors.add(joe)
entry.authors.add(john, paul, george, ringo) # To add multiple records

Entry.objects.filter(pub_date__year=2006) # To get all entries from year 2006

# Chaining Filters
Entry.objects.filter(headline__startswith='What').exclude(pub_date__gte=datetime.date.today()).filter(pub_date__gte=datetime.date(2005, 1, 30)
# or
q1 = Entry.objects.filter(headline__startswith="What")
q2 = q1.exclude(pub_date__gte=datetime.date.today())
q3 = q1.filter(pub_date__gte=datetime.date.today())


Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headline='Hello').   # AND
Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3)).exclude(headline='Hello') # or, more restrictive, so use Q object


# order_by()
Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')
Entry.objects.order_by('?') # random ordering
Entry.objects.order_by('blog__id')  # ordering by related object
Entry.objects.order_by('blog__name')
Entry.objects.order_by(Coalesce('summary', 'headline').desc())
Entry.objects.order_by(Lower('headline').desc())
Entry.objects.order_by() # If you don't want to order by anything
Entry.objects.order_by('headline').order_by('pub_date') # clear previous ordering

# reverse()
my_queryset.reverse()[:5]








