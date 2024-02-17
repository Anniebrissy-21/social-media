from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,FormView,CreateView,DetailView,UpdateView,ListView,TemplateView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

# Create your views here.

from myapp.forms import LoginForm,RegisterForm,ProfileForm,PostForm,StoryForm,CommentForm
from myapp.models import UserProfile,Posts,Stories,Comments

def signin_requied(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Permission Denied")
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

# def owner_permission_required(fn):
#     def wrapper(request,*args,**kwargs):
#         id=kwargs.get("pk")
#         comment_obj=Comments.objects.get(id=id)
#         if comment_obj.user != request.user:
            


dec=[signin_requied,never_cache]

class SignInView(FormView):
    template_name="signin.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                print("Login Success")
                return redirect("index")
                
        print("Invalid Credentials")
        return render(request,"signin.html",{"form":form})

class SignUpView(CreateView):
    template_name="signup.html"
    form_class=RegisterForm
    success_url=reverse_lazy("login")

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")

@method_decorator(dec,name="dispatch")
class IndexView(ListView):
    template_name="index.html"
    context_object_name="data"
    model=Posts 

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super().get_context_data(**kwargs)
        qs=Stories.objects.all()
        context["stories"]=qs
        return context
    

@method_decorator(dec,name="dispatch")
class ProfileCreateView(CreateView):
    template_name="profile.html"
    form_class=ProfileForm
    success_url=reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


@method_decorator(dec,name="dispatch")   
class ProfileDetailView(DetailView):
    template_name="profile_detail.html"
    model=UserProfile
    context_object_name="data"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        qs=self.request.user.post.all()
        context["posts"]=qs
        return context


@method_decorator(dec,name="dispatch") 
class ProfileEditView(UpdateView):
    template_name="profile_edit.html"
    form_class=ProfileForm
    model=UserProfile
    success_url=reverse_lazy("index")
    

@method_decorator(dec,name="dispatch")
class PostCreateView(CreateView):
    template_name="post_create.html"
    form_class=PostForm
    success_url=reverse_lazy("profile")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


@method_decorator(dec,name="dispatch")
class PostEditView(UpdateView):
    template_name="post_edit.html"
    form_class=PostForm
    model=Posts
    success_url=reverse_lazy("index")


class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Posts.objects.get(id=id).delete()
        return redirect("index")

#
@method_decorator(dec,name="dispatch")
class PostLikeView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_obj=Posts.objects.get(id=id)
        user=request.user
        action=request.POST.get("action")
        if action=="like":
            post_obj.liked_by.add(user)
        elif action=="unlike":
            post_obj.liked_by.remove(user)
        return redirect("index")
    
class LikedPostListView(View):
    template_name="post_list.html"
    model=Posts

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        qs=post.liked_by.all()
        return render(request,self.template_name,{"data":qs})

#posts/<int:pk>/save
class PostSaveView(View):
    def post(sef,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_obj=Posts.objects.get(id=id)
        action=request.POST.get("action1")
        if action=="save":
            request.user.profile.saved_post.add(post_obj)
        elif action=="unsave":
            request.user.profile.saved_post.remove(post_obj)
        return redirect("index")
            
class StoryCreateView(CreateView):
    template_name="story_add.html"
    model=Stories
    form_class=StoryForm
    success_url=reverse_lazy("index")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user=self.request.user
        return super().form_valid(form)


@method_decorator(dec,name="dispatch")   
class StoryDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Stories.objects.get(id=id).delete()
        return redirect("index")

@method_decorator(dec,name="dispatch")   
class CommentCreateView(CreateView):
    template_name="comment_add.html"
    form_class=CommentForm
    success_url=reverse_lazy("index")

    # def form_valid(self, form: BaseModelForm) -> HttpResponse:
    #     form.instance.user=self.request.user
    #     return super().form_valid(form)
    
    def post(self,request,*args,**kwargs):
        form=CommentForm(request.POST)
        if form.is_valid():
            id=kwargs.get("pk")
            post_obj=Posts.objects.get(id=id)
            form.instance.post=post_obj
            form.instance.user=request.user
            form.save()
            return redirect("index")
        else:
            return render(request,self.template_name,{"form":form})
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        qs=Comments.objects.all()
        context["comments"]=qs
        return context

# @method_decorator(dec,name="dispatch")
# class CommentListView(View):
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         post_object=Posts.objects.get(id=id)
#         qs=Comments.objects.filter(post=post_object)
#         return render(request,"comment_list.html",{"data":qs})


@method_decorator(dec,name="dispatch")
class CommentDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Comments.objects.get(id=id).delete()
        return redirect("index")

