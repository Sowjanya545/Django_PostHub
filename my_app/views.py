from django.shortcuts import render, redirect
from .forms import UserRegistrationForm,PostForm
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse

#types of views: 1)functions 2)classes

def home(request):
    name ='Sowjanya'
    nums = [1,2,3,4,5,6,7,8,9,10]
    context = {'name':name, 'nums':nums}
    return render(request,'home.html',context)
def login_view(request):
    return render(request,'login.html')

def register(request):
    form=UserRegistrationForm()
    if request.method =='GET':
        return render(request,'register.html',{'form':form})
    if request.method =='POST': # after form submission
        #request.post contains form data

        form=UserRegistrationForm(request.POST)#form filled with data
    if form.is_valid():
        form.save()#create user
        return redirect('login')
    else:
        return render(request,'register.html',{'form':form})
    

def user_login(request):
    if request.method == 'GET':
        return render(request,'login.html')

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)#login user
            return redirect('home')
        else:
            error = 'invalid username or password'
            return render(request, 'login.html',{'error':error})
        
def user_logout(request):
    logout(request)
    return redirect('login')



def posts(request):
    post_list = Post.objects.all().order_by('-updated_at') #select *from post
    return render(request,'posts.html',{'post_list':post_list})

def read_post(request,post_id):
    post = Post.objects.get(pk=post_id) #select *from post where pk=post_id
    return render(request,'read-post.html',{'post':post})


@login_required(login_url='login')
def create_post(request):
    form = PostForm() #empty post form

    if request.method == 'GET':
        return render(request,'create-post.html',{'form':form})
    
    if request.method == 'POST':
        #request.POST contains form data
        #request.FILES contains attachments
        
        form = PostForm(request.POST,request.FILES)

        if  form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # assign user as author
            post.save()
            return redirect('posts')
        else:
            return render(request,'create-post.html',{'form':form})
        
def update_post(request,post_id):
    try:
         post = Post.objects.get(pk=post_id) # get post using id
    except Post.DoesNotExist:
        return HttpResponse('Post does not exit!')
   

    if request.user != post.author:
        return HttpResponse('you are not allowed to update this post')

    form = PostForm(instance=post)

    if request.method == 'GET':
        return render(request,'update-post.html',{'form':form})
    
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=post)

    if form.is_valid():
        post = form.save(commit=False)
        post.updated_at = timezone.now()
        post.save()
        return redirect('posts')
    else:
        return render(request,'update-post.html',{'form':form})
    
def delete_post(request,post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return HttpResponse('Post does not exists!')

    if request.user != post.author:
        return HttpResponse('you are not allowed to delete this post')

    post.delete()
    return redirect('posts')  
    