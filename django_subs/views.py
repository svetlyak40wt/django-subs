from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def subscribe(request):
    from django_subs.utils import subscribe
    subscribe(
        request.POST['subs_id'],
        request.POST['email'],
    )
    return redirect(request.POST['next'])


@require_POST
def unsubscribe(request):
    from django_subs.utils import unsubscribe
    unsubscribe(
        request.POST['hash'],
    )
    return redirect(request.POST['next'])

