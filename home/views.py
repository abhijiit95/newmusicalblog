
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
# Create your views here.
def home(request):
    return render(request,'home/home.html')
    #return HttpResponse('this is home')


def contact(request):
    
    if request.method== 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content= request.POST['content']
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
        print(name, email, phone, content)

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<40:
            messages.error(request, 'please fil the correct values')

        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,'your message has been successfully sent')
    return render(request,'home/contact.html')


def about(request):
    messages.success(request, 'this is about')
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)> 78 :
        allPosts = Post.objects.none()

    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, " no search result is found please refine your query")

    params = {'allPosts': allPosts, "query": query}
    return render(request,'home/search.html',params)


def handleSignup(request):
    if request.method =="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username)> 10:
            messages.error(request,"username is having must be 10 charecters")
            return redirect('home')
            
        if not username.isalnum():
            messages.error(request,"username should havinhg number and charecter both")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request,"password do not match")
            return redirect("home")





        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "your iCoder account has been suceessfully created")

        return redirect("home")
        
    else:
        return HttpResponse("404 - ERROR found")


def handleLogin(request):
    if request.method =="POST":
        loginusername= request.POST['loginusername']
       
        loginpassword= request.POST['loginpassword']
        
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request, "Successfully logged in")
            return redirect('home')

        else:
            messages.error(request, "invalid credentials,please try again")
            return redirect('home')


    return HttpResponse("404 - ERROR found")

 
def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully LoggedOff")
    return redirect('home')    
        
    
    

    