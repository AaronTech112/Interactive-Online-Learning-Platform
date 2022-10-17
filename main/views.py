
from distutils.log import error
from email import message
from pydoc_data.topics import topics
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic , Message, User
from .forms import RoomForm
from .forms import UserForm,UpdateUserForm
from .forms import MyUserCreationForm
#we import the Q modulw which helps us in recieving and filtering queries from the url, and database
from django.db.models import Q
# we import this django user to check if it exist for authentication in line 
# from django.contrib.auth.models import User
# imported a django shortcut that helps us to diplay flash messages in line 
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
# this django decorator allows you to restrict certain views for users that are not logged in with session id in the browser
from django.contrib.auth.decorators import login_required


#rooms=[
#    {'id':1,'name':'Lets Learn Forex'},
#    {'id':2,'name':'Free Account Funding'},
#    {'id':10,'name':'Traders Gist and Outing'},
#    {'id':11,'name':'Traders Gist and Outing'},
#    {'id':12,'name':'Traders Gist and Outing'},
#]

def LoginPage(requset):
    # we use the page variable to store the login string which will be sent in the context dictionary 
    # that will be accessed in the login_register.html template with an if statement that checks if 
    # the page variable is = 'login' and then shows the login form , else it displays the register 
    # form on the same template
    page = 'login'

    if requset.user.is_authenticated:
        return redirect('home')
    wrong=False
    if requset.method == 'POST':
        # we get and store the email and password through the name value in the html input field
        email = requset.POST.get('email').lower()
        password = requset.POST.get('password')

        try:
             # then we check the User model for a matching username
            user = User.objects.get( email = email )
        except:
             #if it doe not match then we can throw a flash message that will be displayed in the included navbar template at the login_register.htmls
             messages.error(requset , ' ')
 
        user = authenticate(requset, username=email , password=password)

        if user is not None:
            login(requset,user)
            return redirect('home')
        else:
            wrong=True

    context = {'page': page,'wrong': wrong}
    return render(requset, 'main/login_register.html', context )
  
def LogoutPage(request):
     logout(request)
     return redirect('home')

def RegisterPage(request):
    #we import the defualt django user creation form here
    form = MyUserCreationForm()
    # one the register button is clicked in the login_register.html template and the form sends the method with value of POST
    if request.method == "POST":
        #then we pass in the values that user has inputed through the form and send it to the Usercreation form
        form = MyUserCreationForm(request.POST)
        # we then process it by checking if the form is valid
        if form.is_valid():
            # then we make sure that the user is created  and usable and accesable by the request and others by passing the commit = False to the save method
            user = form.save(commit=False)
            # we then set the username to lower case incase the person inputs an uppercase letter
            user.username = user.username.lower()
            #before we finally save the user in the database
            user.save()
            #we also want to login the user aftyer creating an account
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong during registration')

    context = { 'form':form}
    return render(request , 'main/login_register.html', context)

def home(request):
    # this is used to filter the search request by finding matching letters 
    q = request.GET.get('q') if request.GET.get('q') !=None else ''

    user_grade = None

    if request.user.is_authenticated:
        user_grade = request.user.grade

        rooms = Room.objects.filter(
            grade = user_grade,
            topic__name__icontains=q,) 

        topics = Topic.objects.filter(
            grade = user_grade,
            name__icontains = q, )

        room_messages = Message.objects.filter(
            house__grade=user_grade,
            house__topic__name__icontains = q,)
    else:
        rooms = Room.objects.all()
        topics = Topic.objects.all()
        room_messages = Message.objects.all()
    
    # use the django count function to count the number rooms available
    room_count = rooms.count()
    
    #we get all the data from the topics table in the database
   
    #this filter allows us to go into the message model, select the room name and check if it contained 
    # in the Q search , which will filter out only the messages whose room name matches the Q search
    # room_messages = Message.objects.filter(Q(house__topic__name__icontains=q))

    #pass the count of the rooms which is used as room_count in the home.html template
    context={'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    
    return render(request,'main/home.html', context )   

# this is the section that contains the users profile
def userProfile(request, pk):
    # we first get the current user by the value of pk that matches the id of the user
    user = User.objects.get(id=pk)
    # then we get all the rooms that was created by the user
    rooms = user.room_set.all()
    # then we get all the messages that was created by the user
    room_messages = user.message_set.all()
    user_grade = request.user.grade
    topics = Topic.objects.filter(grade=user_grade)

    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'main/profile.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    #we are geting all the children of the Message class in the model from the room Class
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            house = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)
        
    context={'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request,'main/room.html',context )

#this is resticted to users that not logged in
@login_required(login_url='/login_page')
def createRoom(request):
    state = 'create'
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.grade = request.user.grade
            room.save()
            return redirect('home')

    context = {'form':form,'topics':topics,'state':state}
    return render(request, 'main/room_form.html', context)

@login_required(login_url='/login_page')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    #we use the request.user method to check if the user logged in is not the owner of the room
    if request.user != room.host:
        # then we restrict him by sending in an http resposne
        return HttpResponse('YOU ARE NOT THE HOST OF THIS ROOM!!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)      
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')        
        room.save()        
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
            
    context={'form':form,'room':room}
    return render(request , 'main/room_form.html', context)

@login_required(login_url='/login_page')
def deleteRoom(request , pk):
    room = Room.objects.get(id=pk)
    # we use the request.user method to check if the user logged in is not the owner of the room
    if request.user != room.host:
        return HttpResponse('YOU ARE NOT THE ALLOWED TO DELETE SOMONES ROOM')
    #we check if the method set in the delete.html button is POST method and then we delte the room
    if request.method == 'POST':
        #we use the room.delete method to simple delete a room
        room.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj':room} )

@login_required(login_url='/login_page')
def deleteMessage(request, pk):
    
    message = Message.objects.get(id=pk)
    if request.user == message.user:
        if request.method == 'POST':
            message.delete()
            return redirect('home')
    else:
        return HttpResponse('YOU ARE NOT THE ALLOWED TO DELETE SOMONES ROOM')

    return render(request, 'main/delete.html',{'obj':message} )

@login_required(login_url='/login_page')
def updateUser(request, pk):
    user = request.user
    form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    return render(request , 'main/update-user.html', {'form':form})

def TopicPage(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    user_grade = request.user.grade
    topics = Topic.objects.filter(
        grade = user_grade,
        name__icontains=q,
        )
    count = topics.count()
    context = {'topics':topics, 'count':count}
    return render(request , 'main/topics.html', context)

def ActivityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request, 'main/activity.html', context)

    












