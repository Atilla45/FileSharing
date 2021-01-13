from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    
)
from .models import Post,SharingFile
import operator
from .forms import CommentForm
from django.urls import reverse_lazy,reverse
from django.contrib.staticfiles.views import serve
from users.models import Profile
from django.db.models import Q




def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'posts':result }
    return render(request,template,context)
   


def getfile(request):
    post = self.get_object()
    if self.request.user != post.author:

        return False
    else:
        return serve(request, 'File')
    
    


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2
    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
class SharedFileView(ListView):
    model = SharingFile
    context_object_name = 'file_list'
    template_name = 'shared_file.html'

    # def get_queryset(self):
    #     user = self.model.objects.filter(user=self.request.user)
    #     file=SharingFile.objects.filter(file=self.kwargs.get('file'))
    #     return SharingFile.objects.filter(user=user,file__in=file).order_by('-date_posted')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=get_object_or_404(SharingFile, user=self.kwargs.get('user'))
        context['file'] = SharingFile.objects.filter(file=self.kwargs.get('file'))
        context['user']=SharingFile.objects.filter(user=user)
        return context



class PostDetailView(FormMixin,DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class=CommentForm
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})


    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = Post.objects.get(id=self.object.id)
        form.instance.post = post
        form.save()
        return super(PostDetailView, self).form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def index(request):
    return HttpResponse('DONE!!!')

