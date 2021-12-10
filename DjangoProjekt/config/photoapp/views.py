# photoapp/views.py
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from django.core.exceptions import PermissionDenied
from django.urls.base import reverse

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy, reverse

from .forms import CommentForm

from .models import Photo, Comment

from django.http import HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse
from django.template import RequestContext


def LikeView(request, pk):
    photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))
    liked = False
    if photo.likes.filter(id=request.user.id).exists():
        photo.likes.remove(request.user)
        liked = False
    else:
        photo.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('photo:detail', args=[str(pk)]))


class PhotoListView(ListView):

    model = Photo

    template_name = 'photoapp/list.html'

    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):

    template_name = 'photoapp/taglist.html'

    # Custom method
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context


class PhotoDetailView(DetailView):

    model = Photo

    template_name = 'photoapp/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PhotoDetailView, self).get_context_data(
            *args, **kwargs)

        stuff = get_object_or_404(Photo, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class PhotoCreateView(LoginRequiredMixin, CreateView):

    model = Photo

    fields = ['title', 'description', 'image', 'tags']

    template_name = 'photoapp/create.html'

    success_url = reverse_lazy('photo:list')

    url = 'https://api.imgflip.com/get_memes'

    def form_valid(self, form):

        form.instance.submitter = self.request.user

        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserIsSubmitter, UpdateView):

    template_name = 'photoapp/update.html'

    model = Photo

    fields = ['title', 'description', 'tags']

    success_url = reverse_lazy('photo:list')


class PhotoDeleteView(UserIsSubmitter, DeleteView):

    template_name = 'photoapp/delete.html'

    model = Photo

    success_url = reverse_lazy('photo:list')


class PhotoCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'photoapp/add_comment.html'
    # fields = '__all__'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('photo:list')
