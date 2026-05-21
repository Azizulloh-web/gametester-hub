from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Game, Review, Category
from .forms import ReviewForm, GameForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator


@login_required
def like_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if game.likes.filter(id=request.user.id).exists():
        game.likes.remove(request.user)  # Убираем лайк
    else:
        game.likes.add(request.user)  # Ставим лайк

    return redirect('game_detail', pk=pk)


@login_required
def edit_game(request, pk):
    game = get_object_or_404(Game, pk=pk)

    # Проверка: только автор может редактировать
    if game.developer != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameForm(instance=game)

    return render(request, 'games/add_game.html', {'form': form, 'edit_mode': True})


# Удаление игры
@login_required
def delete_game(request, pk):
    game = get_object_or_404(Game, pk=pk)

    # Проверка: только автор может удалить
    if game.developer != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        game.delete()
        return redirect('game_list')

    return render(request, 'games/confirm_delete.html', {'game': game})


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_games = profile_user.games.all()
    user_reviews = Review.objects.filter(author=profile_user)

    return render(request, 'games/profile.html', {
        'profile_user': profile_user,
        'user_games': user_games,
        'user_reviews': user_reviews
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('game_list')
    else:
        form = UserCreationForm()

    return render(request, 'games/register.html', {'form': form})


def game_list(request):
    # Получаем параметры
    cat_slug = request.GET.get('category')
    status_val = request.GET.get('status')
    search_q = request.GET.get('search')

    # Стартовый набор игр
    games = Game.objects.all().order_by('-created_at')

    # Применяем фильтры только если они НЕ пустые
    if cat_slug and cat_slug != '':
        games = games.filter(category__slug=cat_slug)

    if status_val and status_val != '':
        games = games.filter(status=status_val)

    if search_q:
        games = games.filter(title__icontains=search_q)

    # Оптимизация
    games = games.select_related('category', 'developer')

    # Пагинация (если она есть, важно передать отфильтрованные игры)
    paginator = Paginator(games, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'games/game_list.html', {
        'page_obj': page_obj,  # используем page_obj в цикле for
        'categories': Category.objects.all(),
        'status_choices': Game.STATUS_CHOICES,
        'current_category': cat_slug,
        'current_status': status_val,
    })


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    reviews = game.reviews.all()

    user_reviewed = False
    if request.user.is_authenticated:
        user_reviewed = Review.objects.filter(game=game, author=request.user).exists()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.author = request.user
            review.save()
            return redirect('game_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'games/game_detail.html', {
        'game': game,
        'reviews': reviews,
        'form': form,
        'user_reviewed': user_reviewed
    })

@login_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user
            game.save()
            return redirect('game_list')
    else:
        form = GameForm()

    return render(request, 'games/add_game.html', {'form': form})

@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk, author=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('game_detail', pk=review.game.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'games/edit_review.html', {'form': form})

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, author=request.user)
    game_pk = review.game.pk
    if request.method == 'POST':
        review.delete()
        return redirect('game_detail', pk=game_pk)
    return render(request, 'games/delete_review.html', {'review': review})