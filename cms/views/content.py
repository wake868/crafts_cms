from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from cms.models import Content, Piece
from django.http import JsonResponse
from ..forms import ContentForm, PieceFormset


# Create your views here.
# content views
def content_index(request, company_id='ac'):
    sort = request.GET.get('sort', 'page_url')
    request.session['company'] = company_id
    contents = get_list_or_404(Content.objects.order_by(sort), company=company_id)

    return render(request, 'cms/content/index.html', {'contents': contents, 'company': company_id})


def content_new(request):
    # if this is a post method then we need to create the new content
    if request.method == 'POST':
        form = ContentForm(request.session, request.POST)
        if form.is_valid():
            new_content = form.save(commit=True)
            if new_content.content_type == 'IMAGE':
                Piece.objects.bulk_create(
                    [
                        Piece(key="image_url", content=new_content),
                        Piece(key="image_link", content=new_content),
                        Piece(key="image_alt", content=new_content)
                    ]
                )
            elif new_content.content_type == 'TEXT':
                Piece.objects.bulk_create(
                    [
                        Piece(key="text_title", content=new_content),
                        Piece(key="text_description", content=new_content),
                    ]
                )
            return redirect('cms:content_index', form.data.get('company'))

    # otherwise show a blank for for entry of a new content
    form = ContentForm(request.session)
    return render(request, 'cms/content/new.html', {'form': form, 'company': request.session['company']})


def content_edit(request, content_id):
    content = get_object_or_404(Content, pk=content_id)

    # if this is a post method then we need to save the updated form data
    if request.method == 'POST':
        form = ContentForm(request.session, request.POST, request.FILES, instance=content)
        formset = PieceFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            edit_content = form.save()
            for form in formset:
                piece = form.save(commit=False)
                piece.content = edit_content
                if piece.key == 'image_url':
                    piece.value = '@hide'
                piece.save()
            return redirect('cms:content_index', form.data.get('company'))

    # otherwise return a form instance for the specified content
    # form = get_content_form(content)
    form = ContentForm(request.session, instance=content)
    formset = PieceFormset(queryset=Piece.objects.filter(content=content))

    return render(request, 'cms/content/edit.html',
                  {
                      'content': content,
                      'form': form,
                      'company': content.company_id,
                      'formset': formset
                  })


def content_delete(request, content_id):
    content = get_object_or_404(Content, pk=content_id)
    if request.method == 'POST':
        content.delete()
        return redirect('cms:content_index', content.company_id)

    return render(request, 'cms/content/delete.html', {'content': content})


# content json
def content_json(request):
    contents = Content.objects.all().values()
    contents_list = list(contents)  # important: convert the QuerySet to a list object
    return JsonResponse(contents_list, safe=False)