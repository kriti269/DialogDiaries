from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, ContactForm, UpdateForm
from .models import Post, User, Comment, ContactUs, Like, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core import serializers
import json


class GetUserDetails(generic.DetailView):
    queryset = User.objects.all()
    template_name = 'post_detail_profile.html'
    context_object_name = "profile_user"


class UserProfileView(generic.DetailView):
    model = User
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        # profile = User.objects.all()
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(User, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context


class ContactView(generic.CreateView):
    form_class = ContactForm
    model = ContactUs
    template_name = 'contact_us.html'
    success_url = '/'


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    login_url = '/sign-in'
    redirect_field_name = 'index.html'
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        return redirect('/')


class UpdatePostView(generic.UpdateView):
    form_class = UpdateForm
    model = Post
    template_name = 'update_post.html'
    success_url = "/"


class GetAllPosts(generic.ListView):
    queryset = Post.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        if filter_val == '':
            filter_val = [x.id for x in Category.objects.all()]
        new_context = Post.objects.filter(
            Q(category__in=filter_val) | Q(category__isnull=True)
        ).order_by('-created_on')
        return new_context

    def get_context_data(self, **kwargs):
        context = super(GetAllPosts, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context


class GetPostDetails(generic.TemplateView):
    def PostDetails(request, slug):
        post = Post.objects.filter(slug=slug)[0]
        template = loader.get_template('post_detail.html')
        comment_count = Comment.objects.filter(post=post).count()
        user = request.user
        user_comment_count = 0
        if not user.is_anonymous:
            user_comment_count = Comment.objects.filter(post=post, posted_by=user).count()
        comment_list = Comment.objects.filter(post=post).order_by('-posted_on')
        like_count = Like.objects.filter(post=post).count()
        context = {'post': post, 'total_comments': comment_count, 'total_likes': like_count,
                   'user_comment_count': user_comment_count, 'comment_list': comment_list}
        return HttpResponse(template.render(context, request))

    def PostDetailsComment(request, slug, showCommentBar):
        post = Post.objects.filter(slug=slug)[0]
        template = loader.get_template('post_detail.html')
        comment_count = Comment.objects.filter(post=post).count()
        user = request.user
        user_comment_count = 0
        if not user.is_anonymous:
            user_comment_count = Comment.objects.filter(post=post, posted_by=user).count()
        comment_list = Comment.objects.filter(post=post).order_by('-posted_on')
        like_count = Like.objects.filter(post=post).count()
        context = {'post': post, 'total_comments': comment_count, 'total_likes': like_count,
                   'showCommentBar': showCommentBar, 'user_comment_count': user_comment_count,
                   'comment_list': comment_list}
        return HttpResponse(template.render(context, request))



class UpdatePost(generic.TemplateView):
    @login_required(login_url='/sign-in')
    def AddLike(request):
        slug = request.GET.get('post', '')
        redirected = request.GET.get('redirect', '')
        post = Post.objects.filter(slug=slug)[0]
        user = request.user
        count = Like.objects.filter(post=post, posted_by=user).count()
        if count == 0:
            Like.objects.create(post=post, posted_by=user)
        if redirected != '' and redirected == 'true':
            return redirect('post_detail', slug)

        like_count = Like.objects.filter(post=post).count()
        comment_count = Comment.objects.filter(post=post).count()
        return JsonResponse({'total_comments': comment_count, 'total_likes': like_count})

    @login_required(login_url='/sign-in')
    def AddComment(request):
        slug = request.GET.get('post', '')
        return redirect('post_detail_comment', slug, "True")

    @login_required(login_url='/sign-in')
    def AddUserComment(request):
        slug = request.GET.get('post', '')
        post = Post.objects.filter(slug=slug)[0]
        user = request.user
        comment_content = request.POST.get('content', '')
        Comment.objects.create(post=post, content=comment_content, posted_by=user)
        user_comment_count = Comment.objects.filter(post=post, posted_by=user).count()
        comment_list = Comment.objects.filter(post=post, posted_by=user)
        like_count = Like.objects.filter(post=post).count()
        comment_count = Comment.objects.filter(post=post).count()
        comment_list = serializers.serialize('json', comment_list)
        return JsonResponse({'total_comments': comment_count, 'total_likes': like_count
                                , 'user_comment_count': user_comment_count
                                , 'comment_list': comment_list})


class GetSignIn(generic.TemplateView):
    model = User
    template_name = 'sign_in.html'


# class CreateBlogPost(generic.TemplateView):
#     model = Post
#     template_name = 'create_blog_post.html'

@csrf_exempt
class GetUserView(generic.TemplateView):
    def LogInUser(request):
        next = request.POST.get('next', '')
        post = request.POST.get('post', '')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email')
        context = {'login_error': None, 'register_error': None, 'register_success': None}
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next is not None and next != '':
                return redirect(next + "?post=" + post + "&redirect=true")

            return redirect('/', {'post_list': Post.objects.order_by('-created_on')})
        else:
            template = loader.get_template('sign_in.html')
            if email != "":
                request_form = request.POST
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    new_user = User.objects.create_user(request_form['username'], request_form['email'],
                                                        request_form['password1'])
                    new_user.first_name = request_form['first_name']
                    new_user.last_name = request_form['last_name']
                    new_user.save()
                    user = authenticate(request, username=new_user.username, password=request_form['password1'])
                    if user is not None:
                        context = {'register_success': 'Registered successfully! Log in now!'}
                        if next is not None and next != '':
                            login(request, user)
                            return redirect(next + "?post=" + post + "&redirect=true")
                    else:
                        context = {'register_error': 'Invalid details! Unable to sign up!'}
                else:
                    context = {'register_error': 'Invalid details! Unable to sign up!'}
            else:
                context = {'login_error': 'Username or Password is invalid!'}

            context["next"] = next
            context["post"] = post
            return HttpResponse(template.render(context, request))

    def LogOut(request):
        logout(request)
        return redirect('/')


class GetPolicy(generic.TemplateView):
    template_name = 'policy.html'


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')


def about(request):
    return render(request, 'about.html')


def getAllCategories(request):
    data = Category.objects.all()
    category_list = serializers.serialize('json', data)
    return HttpResponse(category_list, content_type="text/json-comment-filtered")


def search_post(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)
        return render(request, 'search_post.html', {'searched': searched, 'posts': posts})
    else:
        return render(request, 'search_post.html', {})