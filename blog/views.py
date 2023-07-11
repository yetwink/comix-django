from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Genre, Comics, Volume, Chapter, Picture, Comment, Profile
from .forms import ComicsForm, ChapterForm, PictureForm, LoginForm, RegisterForm, CommentForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
# Create your views here.


def index(request):
    comics = Comics.objects.all()
    top_comics = comics.order_by('views')
    context = {
        'title': 'Главная страница - Комиксы',

        'comics': comics,
        'top_comics': top_comics[:3]
    }

    return render(request, 'blog/index.html', context)


def genre_page(request, pk):
    genre = Genre.objects.get(pk=pk)

    comics = Comics.objects.filter(genres=genre)
    top_comics = comics.order_by('views')
    context = {
        'title': f'Комиксы жанра: {genre}',

        'comics': comics,
        'top_comics': top_comics[:3]
    }

    return render(request, 'blog/index.html', context)


def comic_detail(request, pk):
    comic = Comics.objects.get(pk=pk)
    volumes = Volume.objects.filter(comics=comic)
    chap = []
    for volume in volumes:
        chapters = Chapter.objects.filter(volume=volume)
        chap += chapters
    comments = Comment.objects.filter(comic=comic)
    context = {
        'title': f'Читать :{comic.title}',
        'comic': comic,
        'chapters': chap,
        'comments': comments
    }
    if request.user.is_authenticated:
        context['comment_form'] = CommentForm()

    return render(request, 'blog/comic_detail.html', context)


# TODO - Вывести главы и сделать ссылку на них чтобы смотреть картинки
# TODO - Разбить сайт на куски
# TODO - Создание комикса пользователем
# TODO - Создание томов и глав для комикса пользователем


def add_comics(request):
    if request.method == 'POST':
        form = ComicsForm(request.POST, request.FILES)
        if form.is_valid():
            comics = form.save(commit=False)
            comics.save()
            form.save_m2m()
            return redirect('comic', comics.pk)
    else:
        form = ComicsForm()

    context = {
        'form': form,
        'title': 'Добавление нового комикса'
    }
    return render(request, 'blog/add_comics.html', context)


def volumes_view(request, pk):
    volumes = Volume.objects.filter(comics_id=pk)
    context = {
        'volumes': volumes,
        'comics': Comics.objects.get(pk=pk)
    }
    return render(request, 'blog/volumes.html', context)


def add_volume(request, pk):
    volumes = Volume.objects.filter(comics_id=pk)
    volumes = [i.number for i in volumes]
    max_volume = max(volumes) if volumes else 0
    Volume.objects.create(comics=Comics.objects.get(pk=pk),
                          number=max_volume + 1)
    volumes = Volume.objects.filter(comics_id=pk)
    context = {
        'volumes': volumes,
        'comics': Comics.objects.get(pk=pk)
    }
    return render(request, 'blog/volumes.html', context)


def chapters_view(request, pk, id):
    chapters = Chapter.objects.filter(volume_id=id)
    context = {
        'chapters': chapters,
        'pk': pk,
        'id': id
    }
    return render(request, 'blog/chapters.html', context)


def add_chapter(request, pk, id):
    if request.method == 'POST':
        volume = Volume.objects.get(id=id)
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.volume = volume
            chapter.save()
            return redirect('chapters', pk, id)
    else:
        form = ChapterForm()
    context = {
        'form': form
    }
    return render(request, 'blog/add_chapter.html', context)


def pictures_view(request, comics_id, volume_id, pk):
    chapter = Chapter.objects.get(pk=pk)
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.chapter = chapter
            picture.save()
            return redirect('pictures', comics_id, volume_id, pk)
    else:

        pictures = Picture.objects.filter(chapter=chapter)
        form = PictureForm()
        context = {
            'form': form,
            'pictures': pictures,
            'comics_id': comics_id,
            'volume_id': volume_id
        }
        return render(request, 'blog/pictures.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы успешно вашли в аккаунт')
                return redirect('index')
            else:
                messages.error(request, 'Не верные имя пользователя/пароль')
                return redirect('login')
        else:
            messages.error(request, 'Не верные имя пользователя/пароль')
            print(form.errors)
            return redirect('login')

    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Вход в аккаунт'
    }
    return render(request, 'blog/login.html', context)



def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('index')



def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            messages.success(request, 'Регистрация прошла успешно. Войдите в аккаунт')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }
    return render(request, 'blog/login.html', context)


class UpdateComics(UpdateView):
    form_class = ComicsForm
    template_name = 'blog/add_comics.html'
    model = Comics
    extra_context = {'title': 'Обновление комикса'}


class DeleteComics(DeleteView):
    model = Comics
    context_object_name = 'comic'
    success_url = reverse_lazy('index')


def page_404(request, exception):
    return render(request, '404.html', status=404)


def save_comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.comic = Comics.objects.get(pk=pk)
        comment.save()
        return redirect('comic', pk)


def show_volume_pictures(request, pk):
    chapter = Chapter.objects.get(pk=pk)
    pictures = Picture.objects.filter(chapter=chapter)
    context = {
            'pictures': pictures,
        }
    return render(request, 'blog/pictures.html', context)



def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    comments = Comment.objects.filter(user_id=pk)
    comics = Comics.objects.filter(author_id=pk)
    context = {
        'profile': profile,
        'title': 'Страница пользователя',
        'comments': len(comments),
        'comics': len(comics)
    }
    return render(request, 'blog/profile.html', context)


def search_results(request):
    word = request.GET.get('q')
    comics = Comics.objects.filter(title__icontains=word)
    top_comics = comics.order_by('views')
    context = {
        'title': 'Главная страница - Комиксы',

        'comics': comics,
        'top_comics': top_comics[:3]
    }

    return render(request, 'blog/index.html', context)


from django.views.generic import UpdateView
from .forms import ProfileForm

class EditProfileView(UpdateView):
    form_class = ProfileForm
    model = Profile
    template_name = 'blog/edit_profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)

