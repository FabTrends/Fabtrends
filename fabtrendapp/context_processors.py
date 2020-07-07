from fabtrendapp.models import category


def category_list(request):
    category_list: object = category.objects.all()
    return {'cat': category_list}
