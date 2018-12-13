from django.shortcuts import render, redirect
from facebook.models import Article
from facebook.models import Page
from facebook.models import Comment
# Create your views here.

def play(request):
    return render(request, 'play.html')

def newsfeed(request):
    articles = Article.objects.all()
    page = Page.objects.all()

    for article in articles:
        article.length = len(article.text)

    return render(request, 'newsfeed.html', {'articles': articles, 'page': page})

def detail_feed(request, number):
    article = Article.objects.get(pk=number)
    if request.method == 'POST':
        Comment.objects.create(
            article=article,
            author=request.POST['author'],
            text=request.POST['text'],
            password=request.POST['password']
        )
    return render(request, 'detail_feed.html', {'article': article})

def new_feed(request):
    if request.method == 'POST':
        add_text = '-추신 : 감사합니다. 탱큐'
        new_article = Article.objects.create(
            author=request.POST['author'],
            title=request.POST['title'],
            password=request.POST['password'],
            text=request.POST['content']
        )

        return redirect(f'/feed/{ new_article.pk }')

    return render(request, 'new_feed.html')


def edit_feed(request, number):
    article = Article.objects.get(pk=number)
    if request.method == 'POST':
        if article.password == request.POST['password']:
            article.author = request.POST['author']
            article.title = request.POST['title']
            article.text = request.POST['content']
            article.save()
            return redirect(f'/feed/{ article.pk }')
        else:
            return redirect(f'/fail')

    return render(request, 'edit_feed.html', {'article': article})


def remove_feed(request, number):
    article = Article.objects.get(pk=number)
    if request.method == 'POST':
        if article.password == request.POST['password']:
            article.delete()
            return redirect(f'/')
        else:
            return redirect(f'/fail')

    return render(request, 'remove_feed.html', {'article': article})

def fail(request):
    return render(request, 'fail.html')

def new_page(request):
    if request.method == 'POST':  # 폼이 전송되었을 때만 아래 코드를 실행
        new_page = Page.objects.create(
            master=request.POST['master'],
            name=request.POST['name'],
            text=request.POST['text'],
            category=request.POST['category']
        )
        return redirect('/pages/')

    return render(request, 'new_page.html')

def remove_page(request, pk):
    page = Page.objects.get(pk=pk)

    if request.method == 'POST':
        page.delete()
        return redirect('/pages/')

    return render(request, 'remove_page.html', {'page': page})

def edit_page(request, pk):
    page = Page.objects.get(pk=pk)

    if request.method == 'POST':
        page.master = request.POST['master']
        page.name = request.POST['name']
        page.text = request.POST['text']
        page.category = request.POST['category']
        page.save()
        return redirect('/pages/')

    return render(request, 'edit_page.html', {'page': page })


