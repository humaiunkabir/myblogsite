from multiprocessing import context
from queue import Empty
from urllib import response
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import author, category, article, comment
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import createForm, createAuthor, commentForm
from django.contrib import messages

# Create your views here.


def home(request):

    if request.user.is_authenticated:
        post = article.objects.filter(
            article_author_id=request.user.id).order_by('-id')
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
        paginator = Paginator(post, 24)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "post": page_obj
        }
        return render(request, 'index.html', context)
    else:
        post = article.objects.all().order_by('-id')
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
        paginator = Paginator(post, 24)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "post": page_obj
        }
        return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def getAuthor(request):
    authorinfo = get_object_or_404(author, name=request.user.id)
    return render(request, 'profile.html', {"authorinfo": authorinfo})


def getSingle(request, id):
    singlepost = get_object_or_404(article, pk=id)
    getComment = comment.objects.filter(post=id)
    form = commentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.post = singlepost
        instance.save()
    context = {
        "post": singlepost,
        "form": form,
        "comments": getComment
    }
    return render(request, 'single.html', context)


def getCategoryWisePost(request, id):
    if request.user.is_authenticated:
        post = article.objects.filter(
            category=id, article_author=request.user.id).order_by('-id')
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
        paginator = Paginator(post, 24)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "post": page_obj
        }
        return render(request, 'categorywisepost.html', context)

    else:
        post = article.objects.filter(category=id).order_by('-id')
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
        paginator = Paginator(post, 24)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "post": page_obj
        }
        return render(request, 'categorywisepost.html', context)


def loginsubmit(request):
    if request.user.is_authenticated:
        name = User.get_full_name(request.user)
        request.session['user_name'] = name
        # request.session['user_id'] = auth.id
        post = article.objects.filter(article_author_id=request.user.id)
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
        paginator = Paginator(post, 24)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "post": page_obj
        }
        return render(request, 'index.html', context)
    else:
        if request.method == 'POST':
            username = request.POST.get('uname')
            password = request.POST.get('psw')
            auth = authenticate(request, username=username, password=password)
            print(username, password)
            if auth is not None:
                auth_login(request, auth)
                name = User.get_full_name(auth)
                request.session['user_name'] = name
                # request.session['user_id'] = auth.id
                post = article.objects.filter(article_author_id=auth.id)
                search = request.GET.get('q')
                if search:
                    post = post.filter(
                        Q(title__icontains=search) | Q(body__icontains=search)
                    )
                paginator = Paginator(post, 24)  # Show 25 contacts per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                context = {
                    "post": page_obj
                }
                return render(request, 'index.html', context)
            else:
                messages.add_message(request, messages.ERROR,
                                     'User Name Or Password Incorrect.')
        return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return render(request, "login.html")


def registrationsubmit(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        username = request.POST.get('uname')
        email = request.POST.get('email')
        passw = request.POST.get('psw')
        cpassword = request.POST.get('cpsw')
        if passw == cpassword:
            user = User.objects.create_user(first_name=fname, last_name=lname, username=username,
                                            password=passw, email=email)
            if user is not None:
                user.save()
                DEFAULTIMAGE = 'defaultuser.png'
                profile_picture = DEFAULTIMAGE
                detals = username
                name = user
                authors = author(profile_picture=profile_picture,
                                 name=name, detals=detals)
                authors.save()
                print(username, passw, email)
                messages.add_message(request, messages.SUCCESS,
                                     'User Registration Successfully Completed.')
                return redirect('login')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Password & Confirmed Password Are Not Match')
        return render(request, 'register.html')
    return render(request, 'login.html')


def newposttemplate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            return redirect('home')
        return render(request, 'newpost.html', {"form": form})
    else:
        return redirect('login')


def getpostreport(request):

    authorinfo = get_object_or_404(User, id=request.user.id)
    author_profile = author.objects.filter(name=authorinfo.id)
    if author_profile:
        authorUser = get_object_or_404(author, name=request.user.id)
        post = article.objects.filter(article_author=authorUser.id)
        return render(request, 'postreport.html', {"post": post, "authorinfo": authorUser})
    else:
        form = createAuthor(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = authorinfo
            instance.save()
            return redirect('postreport')
        return render(request, 'createauthor.html', {"form": form})


def getUpdateInfo(request, pid):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(article, id=pid)
        form = createForm(request.POST or None,
                          request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, 'Article Update Completed.')
            return redirect('postreport')
        # else:
        #     messages.error(request, 'Article Update Failed.')
        #     return redirect('postreport')
        return render(request, 'newpost.html', {"form": form})
    else:
        return redirect('login')


def getdeletepost(request, pid):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=pid)
        post.delete()
        return redirect('postreport')
    else:
        return redirect('login')
