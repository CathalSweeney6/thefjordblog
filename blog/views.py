from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Article, Comment, Contact
from .forms import CommentForm, ContactForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


# View for list of posts on home page


class ArticleList(generic.ListView):
    model = Article
    queryset = Article.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

# View for full post in detail


class ArticleDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(status=1)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if article.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "article_detail.html",
            {
                "article": article,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
                "contact_form": ContactForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Article.objects.filter(status=1)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if article.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
        else:
            comment_form = CommentForm()


        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.instance.email = request.user.email
            contact_form.instance.name = request.user.username
            contact = contact_form.save(commit=False)
            contact.article = article
            contact.save()
        else:
            contact_form = ContactForm()

        return render(
            request,
            "article_detail.html",
            {
                "article": article,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked,
                "contact_form": contact_form
            },
        )


# View for liking a post


class ArticleLike(View):

    def post(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Article, slug=slug)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)

        return HttpResponseRedirect(reverse('article_detail', args=[slug]))


# View for searching for a post


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']

        query = Q(content__icontains=searched) | Q(title__icontains=searched)
        article_list = Article.objects.filter(query)

        return render(request, 'search.html',
                      {'searched': searched, 'article_list':  article_list})
    else:
        return render(request, 'search.html', {})


# View for the contact form

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')            
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


# View for the success message page


def success(request):
    if request.method == "POST":
        # success = request.POST['success']
        print("if block")
        return render(request, 'success.html')

    else:
        print("else block")
        return render(request, 'success.html', {})


# View for deleting a comment as Site User

@login_required
def delete_user_comment(request, comment_id):
    """ Delete comment
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Your comment was deleted successfully')
    return HttpResponseRedirect(reverse(
        'article_detail', args=[comment.article.slug]))

# View for editing a comment as Site User


class EditComment(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit comment
    """
    model = Comment
    template_name = 'edit_user_comment.html'
    form_class = CommentForm
    success_message = 'Your comment was successfully updated, Skål!'
