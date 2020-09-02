from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User, auth
from polls.models import Post
from polls.models import Profile
from .forms import ProfilePicUpdateForm, UserProfileUpdateForm

'''
types of django messages--------->
messgaes.success
messgaes.error
messgaes.warning
messgaes.info
messgaes.debug
'''

def register(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		fname = request.POST['fname']
		fname = fname.capitalize()
		lname = request.POST['lname']
		lname = lname.capitalize()
		if password1 == password2:
			if not User.objects.filter(username=username).exists():
				user = User.objects.create_user(username=username, password=password1, first_name=fname, last_name=lname, email=email)
				p = Profile.objects.create(user=user)
				p.save()
				user.save()
				messages.success(request, f'{fname} your account created successfully. Now you can login here.')
				return redirect('polls-signin')
			else:
				messages.info(request, f'Username {username} already taken')
				return render(request, 'users/register.html', {'fname': fname, 'lname': lname})
		else:
			print("password not match")
			return render(request, 'users/register.html')
	elif request.user.is_authenticated:
		return redirect("polls-home")

	else:
		return render(request, 'users/register.html', {'title': 'Register'})

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		messages.success(request, f'Loggout successfully')
		return redirect('polls-home')
	else:
		return redirect('polls-home')

def newPost(request):
	if request.method == 'POST':
		ttl = request.POST['title']
		content = request.POST['content']
		author = request.user.username
		author = User.objects.get(username=author)
		post = Post(title=ttl, content=content, author=author)
		post.save()
		messages.success(request, 'Post created successfully.')
		return redirect('polls-home')
	elif not request.user.is_authenticated:
		return redirect('polls-home')
	else:
		return render(request, 'users/newpost.html')

def profile(request):
	if not request.user.is_authenticated:
		return redirect('polls-home')
	else:
		user = User.objects.filter(username=request.user.username).first()
		posts = Post.objects.filter(author=user).order_by('-date_posted')
		context = {
			'title': request.user.first_name,
			'posts': posts,
			'pic': user.profile.image.url,
		}
		return render(request, 'users/profile.html', context)

def edit(request, pk):
	if request.method == "POST":
		newTitle = request.POST['title']
		newContent = request.POST['content']
		user = User.objects.get(username=request.user.username)
		post = Post.objects.get(id=pk, author=user)
		post.title = newTitle
		post.content = newContent
		post.save()
		messages.success(request, 'Post updated')
		return redirect('profile')


	elif not request.user.is_authenticated:
		return redirect('polls-home')
	else:
		print(pk)
		user = User.objects.filter(username=request.user.username).first()
		try:
			post = Post.objects.get(id=pk, author=user)
		except:
			return redirect('polls-home')
		context = {
			'post_title': post.title,
			'content':	post.content,
			'title': 'edit',
			'pk': pk
		}
		return render(request, 'users/editPost.html', context)

def fetchProfile(request, username):
	try:
		u = User.objects.get(username=username)
		if u == request.user:
			return redirect('profile')
	except:
		return redirect('polls-home')
	posts = Post.objects.filter(author=u).all()
	context = {
		'u': u,
		'posts': posts,
		'title': u.username,
	}
	try:
		if u.profile:
			context['pic'] = u.profile.image.url
	except:
		pass
	return render(request, 'users/fetchProfile.html', context)

def changePassword(request):
	if not request.user.is_authenticated:
		return redirect('polls-home')
	elif request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Password Updated')
			return redirect('profile')
		else:
			messages.info(request, 'Please enter correct details')
			return redirect('change-password')
	else:
		form = PasswordChangeForm(request.user)
		context = {
			'title': 'Update password',
			'form': form
		}
		return render(request, 'users/changePassword.html', context)


def editProfile(request):
	if not request.user.is_authenticated:
		return redirect('polls-home')
	elif request.method == 'POST':
		p_form = ProfilePicUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		u_form = UserProfileUpdateForm(request.POST, instance=request.user)
		if p_form.is_valid() and u_form.is_valid():
			p_form.save()
			u_form.save()
			messages.success(request, 'Profile Update.')
			return redirect('profile')
		else:
			messages.info(request, f'Username already taken')
			return redirect('edit-profile')
	else:
		u_form = UserProfileUpdateForm(instance=request.user)
		p_form = ProfilePicUpdateForm(instance=request.user.profile)
		context = {
			'u_form': u_form,
			'p_form': p_form,
			'title' : 'Profile Update',
		}
		return render(request, 'users/edit-profile.html', context)

def removePost(request, pid):
	if not request.user.is_authenticated:
		return redirect('polls-home')
	else:
		Post.objects.get(id=pid).delete()
		messages.success(request, 'Post deleted.')
		return redirect('profile')

def post_detail(request, pid):
	post = Post.objects.get(id=pid)
	is_liked = False
	is_favourite = False
	
	if post.like.filter(id=request.user.id).exists():
		is_liked = True
	
	if post.favourite.filter(id=request.user.id).exists():
		is_favourite = True
	

	total_likes = post.like.count()
	context = {
		'title': post.title,
		'is_favourite': is_favourite,
		'post': post,
		'is_liked': is_liked,
		'total_likes': total_likes,
	}
	return render(request, 'users/post-detail.html', context)

def like(requests):
	post = Post.objects.get(id=requests.POST.get('like'))
	is_liked = False
	if post.like.filter(id=requests.user.id).exists():
		post.like.remove(requests.user)
		is_liked = False
	else:
		post.like.add(requests.user)
		is_liked = True
	return redirect('post-detail', pid=post.id, )

def favourite(requests):
	post = Post.objects.get(id=requests.POST.get('favourite'))
	is_favourite = False
	if post.favourite.filter(id=requests.user.id).exists():
		post.favourite.remove(requests.user)
		is_favourite = False
	else:
		post.favourite.add(requests.user)
		is_favourite = True
	return redirect('post-detail', pid=post.id)

def list_favourites(request):
	if not request.user.is_authenticated:
		return redirect('polls-home')
	u = request.user
	posts = u.favourites.all()
	context = {
		'posts': posts,
		'title': 'Favourite',
	}
	return render(request, 'users/list-favourites.html', context)
