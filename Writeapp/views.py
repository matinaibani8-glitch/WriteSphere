from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import logout
from .forms import userform,storyform,BlogCommentForm,updateform,updatesign
from .models import usersign,story,BlogLike,Follow
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    posts = story.objects.all().order_by('-created_at')
    posts = story.objects.all()

    gmail = request.session.get('gmail')
    current_user = usersign.objects.filter(gmail=gmail).first()

    following_ids = []

    if current_user:
        following_ids = list(
            Follow.objects.filter(
            follower=current_user
        ).values_list('following_id', flat=True)
    )

    comment_form = BlogCommentForm()
    return render(request,"index.html",{"posts":posts,'comment_form': comment_form,'current_user': current_user,'following_ids': following_ids,})

def signup(request):
    if request.method == "POST":
        user = userform(request.POST)
        if user.is_valid():
            user.save()
            print("Data Saved!")
            return redirect("home")
        else:
            print(user.errors)
    return render(request,"Signup.html")

def login(request):
    if request.method == "POST":
        unm = request.POST['gmail']
        pas = request.POST['password']

        user = usersign.objects.filter(gmail=unm,password=pas).first()

        uid = usersign.objects.get(gmail=unm)

        if user:
            request.session['gmail'] = user.gmail
            request.session['uid'] = uid.id

            print("Login Successfull!")
            return redirect("home")
        else:
            print("Error!")
    return render(request,"login.html")

def create(request):
    if request.method == "POST":
        gmail = request.session.get("gmail")

        if not gmail:
            return redirect('login')

        author_user = usersign.objects.filter(gmail=gmail).first()

        if not author_user:
            return redirect('login')

        user = storyform(request.POST,request.FILES)

    
        if user.is_valid():
            new_story = user.save(commit=False)
            new_story.author = author_user
            new_story.save()
            
            print("Story Uploaded on Data Base")
            return redirect("profile")
        else:
            print(user.errors)
    return render(request,"create-post.html")

def profile(request):
    unm = request.session.get('gmail')

    if not unm:
        return redirect('login')

    user = usersign.objects.filter(gmail=unm).first()

    if not user:
        return redirect('login')

    posts = story.objects.filter(author=user).order_by('-created_at')
    print(posts)
    messages.info(request,"Welcome")
    
    return render(request,"profile.html",{"cuser":user,"posts":posts})

def blog(request):
    return render(request,"blog-detail.html")

def userlogout(request):
    logout(request)
    return redirect("home")


@require_POST
def like_post(request, post_id):
    gmail = request.session.get('gmail')

    if not gmail:
        return redirect('login')

    user = get_object_or_404(usersign, gmail=gmail)
    post = get_object_or_404(story, pk=post_id)

    like, created = BlogLike.objects.get_or_create(
        user=user,
        post=post
    )

    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def add_comment(request, post_id):
    gmail = request.session.get('gmail')

    if not gmail:
        return redirect('login')

    user = get_object_or_404(usersign, gmail=gmail)
    post = get_object_or_404(story, pk=post_id)

    form = BlogCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = user
        comment.post = post
        comment.save()
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Please enter a valid comment.')

    return redirect(request.META.get('HTTP_REFERER', '/'))

def Edit(request, id):
    user = request.session.get('gmail')

    if not user:
        return redirect('login')

    cid = story.objects.get(id=id)

    if request.method == "POST":
        form = updateform(request.POST, instance=cid)

        if form.is_valid():
            form.save()
            print("Story Updated!")
            return redirect("profile")
    else:
        form = updateform(instance=cid)

    return render(request, "Edit_Story.html", {
        'cuser': user,
        'uid': cid,
        'form': form
    })


def delete(request,id):
    stid = story.objects.get(id=id)
    story.delete(stid)
    return redirect("/")

def ed_profile(request,id):
    user = request.session.get('gmail')

    cid = usersign.objects.get(id=id)

    if request.method == "POST":
        update = updatesign(request.POST,instance=cid)

        if update.is_valid():
            update.save()
            print("Your Profile Updated!")
            return redirect("/")
        else:
            print(update.errors)
    return render(request,"Edit_profile.html",{"uid":cid})

def search(request):
    keyword = request.GET.get('q','')
    print(keyword)
    user = story.objects.filter(title__icontains=keyword)
    return render(request,"search.html",{"cuser":user})

def category(request):
    keyword = request.GET.get('q','')
    print(keyword)
    user = story.objects.filter(category__iexact=keyword)
    return render(request,"category.html",{"cuser":user})

def author_search(request):
    author_id = request.GET.get('author')
    print("Selected Author ID:", author_id)

    if author_id:
        cuser = story.objects.filter(author_id=author_id)
    else:
        cuser = story.objects.all()

    for s in cuser:
        print("Story:", s.title)
        print("Author ID:", s.author_id)

    authors = usersign.objects.all()

    for a in authors:
        print(a.id,a.firstname,a.lastname)

    return render(request, "author_search.html", {"cuser": cuser,"authors": authors})


def follow_user(request, id):
    if request.method == "POST":

        # Logged-in user ko find karna
        gmail = request.session.get('gmail')

        if not gmail:
            return redirect('login')

        current_user = usersign.objects.filter(gmail=gmail).first()

        if not current_user:
            return redirect('login')

        # Jise follow karna hai, us user ko find karna
        target_user = usersign.objects.filter(id=id).first()

        if not target_user:
            return redirect('/')

        # Apne aap ko follow nahi kar sakte
        if current_user.id == target_user.id:
            return redirect('/')

        # Pehle se follow hai to Unfollow, warna Follow
        follow = Follow.objects.filter(
            follower=current_user,
            following=target_user
        )

        if follow.exists():
            follow.delete()
        else:
            Follow.objects.create(
                follower=current_user,
                following=target_user
            )

    return redirect('/')
