from django.shortcuts import render

from forms import Form

def main(request):
    form = Form()
    return render(request, 'template.html', {'form': form})
