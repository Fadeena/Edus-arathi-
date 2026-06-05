from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from .models import Profile,Course,Material,TutorChat
from django.shortcuts import render, get_object_or_404

from django.contrib import messages
from .forms import  CourseForm,MaterialForm,AipromptForm
import PyPDF2
import docx

def homefun(request):
     return render(request,'home.html')
def adminfun(request):
    return render(request,'adminhome.html')
def tutorfun(request):
    return render(request,'tutorhome.html')
def studentfun(request):
    return render(request,'studenthome.html')
def aboutusfun(request):
    return render(request,'aboutus.html')
def contactusfun(request):
    return render(request, 'contactus.html')

def explorecoursesfun(request):
    courses = Course.objects.all()
    return render(request, "explorecourses.html", {'courses': courses})

def loginfun(request):
    if request.method == 'POST':
        uname=request.POST['username']
        p1=request.POST['pwd1']
        user=auth.authenticate(username=uname,password=p1)
        if user:
            auth.login(request,user)
            if user.is_superuser:
                return redirect('admin')
            elif user.is_staff:
                return redirect('tutor')
            else:
                # Optional: Double check if a Profile exists to confirm they are a registered student
                if Profile.objects.filter(user=request.user).exists():
                    return redirect('student')
                else:
                    return redirect('register')
        else:
            return render(request, 'login.html', {'er': 'Invalid credentials'})
            
    return render(request, 'login.html')
    #         auth.login(request,x)
    #         a=Profile.objects.filter(us=request.user).exists()
    #         if a:
    #             return redirect('/Home')
    #         else:
    #             return redirect('/register')
    #     else:
    #         return render(request,'login.html',{'er':'invalid username and password'})
    # else:
    #     return render(request,'login.html')


def registerfun(request):
    if request.method == "POST":
        uname=request.POST['username']
        full_name=request.POST['full_name']
        email=request.POST['email']
        mobile=request.POST['mobile']
        dob=request.POST['dob']
        gender=request.POST['gender']
        education=request.POST['education']
        course=request.POST['course']
        role=request.POST['role']
        p1=request.POST['pwd1']
        p2=request.POST['pwd2']
        if p1==p2:
            if User.objects.filter(username=uname).exists():
                return render(request,'register.html',{'er':"Username already Exist"})
            elif User.objects.filter(email=email).exists():
                return render(request,'register.html',{'er':"Email already Exist"})
            else:
                user = User.objects.create_user(username=uname,email=email,password=p1,
                first_name = full_name,
                is_staff=(role=='tutor'),  
                is_active=False
                )
                user.save()
            # 4. Create the Profile linked to that user
                Profile.objects.create(user=user,mobile=mobile,dob=dob,gender=gender,
                    education_level=education,
                    course_preference=course,
                    role=role
                )
                return render(request,'login.html',{'er':'Registration successful! Waiting for Admin Approval.'}) 
        else:
            return render(request,'register.html',{'er':"Password not Matching"})


    return render(request, 'register.html')



################  ADMIN   ###################

def userlistfun(request):

    u=User.objects.filter(is_superuser=False,is_staff= False)
    t=User.objects.filter(is_superuser=False,is_staff=True)
    pending=User.objects.filter(is_active=False)
    return render(request,'aduserlist.html',{'us':u,'tu':t,'pen':pending})

def approveuserfun(request,uid):

    a = User.objects.get(id=uid)
    a.is_active = True
    a.save()
    return redirect('pendinguser')

def pendinguserfun(request):

    pending = User.objects.filter(is_active=False)
    return render(request,'adapproveuser.html',{'pen': pending})

def addcoursefun(request):
    if request.method=='POST':
        f=CourseForm(request.POST)
        if f.is_valid():
            f.save()
            return render(request,'adminhome.html',{'er':'Course Added successfully'})

    else:
        f=CourseForm()
        return render(request,'adaddcourse.html',{'fm':f})
def viewcoursefun(request):
    courses = Course.objects.all()
    return render(request, 'viewcourses.html',{'courses': courses})


def userdetailfun(request,u_id):
    target_user = get_object_or_404(User, id=u_id)
    profile = target_user.profile
    current_role = profile.role.lower()
    if current_role == 'tutor':
        my_courses = target_user.teaching_courses.all()
    else:
        my_courses = target_user.setcourses.all()

    return render(request, 'viewdetails.html', {'target_user': target_user,
    'profile': profile,
    'my_courses': my_courses})


def logoutfun(request):
    auth.logout(request)
    return redirect('/login')




########## TUTOR ##########
def mycoursefun(request):
    if request.method=="POST":
        selectedcourses=request.POST.getlist('courses')
        request.user.teaching_courses.set(selectedcourses)
        return redirect('mycourse')

    return render(request,'mycourse.html',{'courses': Course.objects.all(),
        'my_courses': request.user.teaching_courses.all()})


def uploadfun(request):
    if request.method=='POST':
        f=MaterialForm(request.POST,request.FILES)
        if f.is_valid():
            m=f.save(commit=False)
            m.tutor=request.user
            m.save()
            return redirect('/uploadlist')
    else:
        f=MaterialForm()
        return render(request,'materialupload.html',{'form':f})


def uploadlistfun(request):
    m=Material.objects.all()
    return render(request,'uploadlist.html',{'material':m})


# def aipromptlabfun(request):
#     if request.method=='POST':
#         f=AipromptForm(request.POST)
#         f.fields['course'].queryset=request.user.teaching_courses.all()
#         if f.is_valid():
#             prompt=f.save(commit=False)
#             prompt.tutor=request.user
#             prompt.save()
#             return redirect('/aipromptlab')
#     else:
#         f=AipromptForm()
#         f.fields['course'].queryset = request.user.teaching_courses.all()
#         return render(request,'aipromptlab.html',{'form':f})
             
# huggingface_hub


def quizgeneratorfun(request):
    if request.method=="POST":
        topic = request.POST.get("topic")
        prompt = f"Create 5 multiple choice quiz questions about {topic}"
        res = client.chat_completion(
            model="meta-llama/Llama-3.2-1B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            stream=False
        )
        quiz = res.choices[0].message.content

        return render(request, "quizgenerator.html",{"quiz": quiz})
            
    else: 
            return render(request, "quizgenerator.html")
def studentlistfun(request):
    studentlist=User.objects.filter(
        is_staff=False, is_superuser=False)
    return render(request,'tustudentlist.html',{'studlist':studentlist})


def tuviewdetailfun(request,u_id):
    target_user = get_object_or_404(User, id=u_id)
    profile = target_user.profile
    if profile.role.lower() != 'student':
        return redirect('/studentlist')

    my_courses = target_user.setcourses.all()

    return render(request, 'tuviewdetail.html', {
        'target_user': target_user,
        'profile': profile,
        'my_courses': my_courses
    })


############### STUDENT ########################
def choosecoursefun(request):
    if request.method=="POST":
        selectedcourses=request.POST.getlist('courses')
        request.user.setcourses.set(selectedcourses)
        return redirect('/choosecourse')
   
    return render(request,'choosecourse.html',{'courses':Course.objects.all(),
     'my_courses':request.user.setcourses.all()})



#huggingface_hub 
def studyplanfun(request):
    username=request.user.first_name
    my_courses=request.user.setcourses.all()
    course_names=", ".join([course.name for course in my_courses])
    if not course_names:
        course_names="General Studies"
    prompt=f"""create a personaized 7 day study plan for{'username'}.
    selected courses:{course_names}
    Include:
    1.Daily learning topics
    2.Practice Tasks
    3.Revision Tasks
    4.Motivation tip
    keep it simple for students."""
    res=client.chat_completion(
        model="meta-llama/Llama-3.2-1B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        stream=False
    )
    plan=res.choices[0].message.content
    return render(request,'studyplan.html',{'plan':plan,'courses':my_courses})

#huggingface_hub 

def readfile(file):
    text=""
    if file.name.endswith(".txt"):
        text=file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        pdf_reader=PyPDF2.PdfReader(file)
        for  page in pdf_reader.pages:
            text+=page.extract_text()+"\n"
    elif file.name.endswith(".docx"):
        doc=docx.Document(file)
        for para in doc.paragraphs:
            text+=para.text+"\n"
    elif file.name.endswith(".jpg",".jpeg",".png"):
        text="An image was uploaded. Please describe or analyze the visible content."

    return text       


def aitutorchatfun(request):
    reply=""
    if request.method=="POST":
        message = request.POST.get("message")
        uploaded_file = request.FILES.get("file")
        prompt = message
        if uploaded_file:
            file_content=readfile(uploaded_file)
            prompt += f"""Student uploaded a file Analyze the content and answer based on it 
            File Content:{file_content}
            Student Question:{message}"""
        res=client.chat_completion(
            model="meta-llama/Llama-3.2-1B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            stream=False
        )   
        reply = res.choices[0].message.content
        return render(request,'aitutorchat.html',{'reply':reply})
    return render(request,'aitutorchat.html')

def activecoursesfun(request):
    activecourses=request.user.setcourses.all()
    return render(request,"activecourse.html",{'activecourses':activecourses})

def quizfun(request):
     return render(request,'quiz.html')


#huggingface_hub 


def viewquizfun(request):  
    student=request.user
    courses=student.setcourses.all()
    quiz=""
    if request.method=="POST":
        for course in courses:
            prompt=f"""create 10 MCQ questions from {course.name}
            Format:
            1.Question
            A)
            B)
            C)
            D)
            Answer:"""
            res=client.chat_completion(
                model="meta-llama/Llama-3.2-1B-Instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,
                stream=False
            )
            quiz+=f"\n\n===={course.name}====\n"
            quiz+=res.choices[0].message.content
    return render(request,'viewquiz.html',{"quiz":quiz,"courses":courses})

#huggingface_hub 

def libraryfun(request):

    student = request.user
    courses = student.setcourses.all()
    materials = Material.objects.filter(course__in=courses).order_by('uploaded_at')

    return render(request, 'library.html', {'materials': materials})

def studentchatfun(request,tutor_id):
    tutor=get_object_or_404(User, id=tutor_id)
    if request.method == "POST":
        msg = request.POST.get("message")

        TutorChat.objects.create(
            student=request.user,
            tutor=tutor,
            sender=request.user,
            message=msg
        )
        return redirect('studentchat', tutor_id=tutor.id)

    chats = TutorChat.objects.filter(
        student=request.user,
        tutor=tutor
    ).order_by('-created_at')
    return render(request, 'studentchat.html', {'tutor': tutor, 'chats': chats})


def tutorchatfun(request):
    chats = TutorChat.objects.filter(
        tutor=request.user
    ).order_by('-created_at')

    return render(request, 'tutorchat.html', {'chats': chats})

def replyfun(request, chat_id):
    chat = get_object_or_404(TutorChat, id=chat_id)

    if request.method == "POST":
        reply = request.POST.get("reply")
        chat.reply = reply
        chat.save()

    return redirect('tutorchat')

def chatselectfun(request):
    tutors = User.objects.filter(profile__role__iexact='tutor')
    return render(request, 'chatselect.html', {'tutors': tutors})