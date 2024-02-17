from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Movie
from .forms import ReviewForm, Review
from django.contrib.auth.decorators import login_required

  
def home(request):
  searchTerm = request.GET.get('searchMovie')
  if searchTerm:
    movies = Movie.objects.filter(title__icontains=searchTerm)
  else:
    movies = Movie.objects.all()
  

  

  return render(request, 'index.html', {'searchTerm':searchTerm, 'movies':movies})


def detail(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)
  reviews = Review.objects.filter(movie=movie)


  return render(request, 'movie_detail.html', {'movie':movie, 'reviews':reviews})


def about(request):
  
  return render(request, 'about.html')


@login_required
def createreview(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)
  form = ReviewForm()
  if request.method == 'GET':
    return render(request, 'createreview.html', {'movie':movie, 'form':form})
  else:
    try:
      form = ReviewForm(request.POST)
      newReview = form.save(commit=False)
      newReview.user = request.user
      newReview.movie = movie
      newReview.save()

      return redirect('detail', newReview.movie.id)

    except ValueError:
      return render(request, 'createreview.html', {'form':form, 'error':'Mauvaise information'})

@login_required

def updatereview(request, review_id):
  review = get_object_or_404(Review, pk=review_id, user=request.user)
  if request.method == 'GET':
    form = ReviewForm(instance=review)
    return render(request, 'updatereview.html', {'form':form, 'review':review})

  else:
    try:
      form = ReviewForm(request.POST, instance=review)
      form.save()
      return redirect('detail', review.movie.id)
    except ValueError:
      return render(request, 'updatereview.html', {'form':form, 'review':review, 'error':'Mauvais commentaire'})


@login_required
def deletereview(request, review_id):
  review = get_object_or_404(Review, pk=review_id, user = request.user)
  review.delete()
  return redirect('detail', review.movie.id)