from django.shortcuts import render

from forms import Form

def main(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            print('keywods: %s' % keywords)
    form = Form()
    return render(request, 'template.html', {'form': form})
