from django.shortcuts import render
from postsapp.models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
#def postlistview(request):
#    post=Post.objects.all()
#    return render(request,'postsapp/postlist.html',{'p':post})

def postlistview(request):
    post=Post.objects.all()
    paginator=Paginator(post,3)
    page_number=request.GET.get('page')
    try:
        post=paginator.page(page_number)
    except PageNotAnInteger:
        post=paginator.page(1)
    except EmptyPage:
        post=paginator.page(paginator.num_pages)
    return render(request,'postsapp/postlist.html',{'p':post})

from django.views.generic import ListView
#class PostListView(ListView):
#    model=Post
#    paginate_by=2
#    template_name='postsapp/postlist.html'
from postsapp.models import Comment
from postsapp.forms import CommentForm
def postdetail_view(request,year,month,day,post):
    postd=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)

    #comments=post.comments.filter(active=True)     --- There is a problem with this line
    csubmit=False
    if request.method=='POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=postd
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'postsapp/postdetail.html',{'pd':postd,'fd':form,'csubmit':csubmit})  #,'comments':comments

from django.core.mail import send_mail
from postsapp.forms import EmailSendForm

def mailsendview(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            p_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],post.title)
            message='Read Post At:\n {}\n\n\'Comments:\n{}'.format(p_url,cd['name'],cd['comments'])
            send_mail(subject,message,'gln@blog.com',[cd['to']])
            sent=True
    else:
        form=EmailSendForm()
        return render(request,'postsapp/sharebyemail.html',{'po':post,'fo':form,'sent':sent})
