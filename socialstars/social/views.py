from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from social.forms import PostForm
from social.models import Post, Friend, Preference


class SocialHome(TemplateView):
    template_name = 'social/home.html'

    def get(self, request):
        form = PostForm()
        posts = Post.objects.all().order_by('-created')
        users = User.objects.exclude(id=request.user.id)
        user = request.user
        try:
            friend = Friend.objects.get(current_user=user)
            friends = friend.users.all()
        except Friend.DoesNotExist:
            friends = None

        args = {'form': form, 'posts': posts, 'users': users,
                'friends': friends, 'user': user}
        return render(request, self.template_name, args)

    def post(self, request):
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            if 'post_image' in request.FILES:
                post.post_image = request.FILES['post_image']

            post.save()
            form = PostForm()
            return redirect('social:home')

        return render(request, self.template_name, {'form': form})


@login_required()
def post_preference(request, post_id, user_pref):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        try:
            pref = Preference.objects.get(user=request.user, post=post)
            pref_value = pref.value

            pref_value = int(pref_value)
            user_pref = int(user_pref)

            if pref_value != user_pref:
                pref.delete()

                upref=Preference()
                upref.user = request.user
                upref.post = post
                upref.value = user_pref

                if user_pref == 1 and pref_value != 1:
                    post.likes += 1
                    post.dislikes -= 1
                elif user_pref == 2 and pref_value != 2:
                    post.dislikes += 1
                    post.likes -= 1

                upref.save()
                post.save()

                return redirect('social:home')

            elif pref_value == user_pref:
                pref.delete()

                if user_pref == 1:
                    post.likes -= 1
                elif user_pref == 2:
                    post.dislikes -= 1

                post.save()
                return redirect('social:home')

        except Preference.DoesNotExist:
            upref = Preference()

            upref.user = request.user
            upref.post = post
            upref.value = user_pref

            user_pref = int(user_pref)

            if user_pref == 1:
                post.likes += 1
            elif user_pref == 2:
                post.dislikes += 1

            upref.save()
            post.save()

            return redirect('social:home')

        else:
            post = get_object_or_404(Post, id=post_id)
            return redirect('social:home')


@login_required()
def connect(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
    elif operation == 'remove':
        Friend.unfriend(request.user, new_friend)
    return redirect('social:home')


@login_required()
def update_post(request, post_id):
    post_id = int(post_id)
    try:
        post_up = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return redirect('social:home')
    post_form = PostForm(request.POST or None, instance=post_up)
    if post_form.is_valid():
        post_form.save()
        return redirect('social:home')

    return render(request, 'social/home.html', {'post_form': post_form})


@login_required()
def delete_post(request, post_id):
    post_id = int(post_id)
    try:
        post_del = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return redirect('social:home')
    post_del.delete()
    return redirect('social:home')


