from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response


class TimeStatus(APIView):
    """API для выведения списка всех уроков по всем продуктам к которым пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра."""

    def get(self, request):
        user = request.user
        queryset = Lesson.objects.filter(product__users=user)
        time_status = []

        for lesson in queryset:
            view = Viewing.objects.get(lesson=lesson, user=user)
            if view.viewing_time:
                view.set_result()
                viewing_time = view.viewing_time
                result = view.result
            else:
                view.set_result()
                viewing_time = 0
                result = view.result
            x = {
                'username': user.username,
                'lesson_name': lesson.name,
                'viewing_time': viewing_time,
                'result': result,
            }
            if x in time_status:
                continue
            else:
                time_status.append(x)
        return Response(time_status)


class ProductApi(APIView):
    """API с выведением списка уроков по конкретному продукту к которому пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра, а также датой последнего просмотра ролика."""

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        product = Product.objects.get(id=pk)
        user = request.user
        queryset = Lesson.objects.filter(product__users=user, product__id=pk)
        product_api = []

        for lesson in queryset:
            view = Viewing.objects.get(lesson=lesson, user=user)
            if view.viewing_time:
                view.set_result()
                viewing_time = view.viewing_time
                result = view.result
            else:
                view.set_result()
                viewing_time = 0
                result = view.result
            product_api.append({
                'product_name': product.owner,
                'lesson_name': lesson.name,
                'viewing_time': viewing_time,
                'result': result,
                'last_view': view.last_view
            })

        return Response(product_api)


class StatisticApi(APIView):
    """API для отображения статистики по продуктам."""

    def get(self, request):
        products = Product.objects.all()
        students = len(User.objects.all())
        statistic = []

        for product in products:
            users = product.users.all()
            lessons = Lesson.objects.filter(product=product)
            result = len(list(Viewing.objects.filter(result='Просмотрено', lesson__in=lessons)))
            all_time = Viewing.objects.filter(lesson__in=lessons).values('viewing_time')
            sum_time = 0
            for time in all_time:
                sum_time += time['viewing_time']
            all_users = len(users)
            percent = (all_users / students) * 100
            statistic.append({
                'owner': product.owner,  # Название
                'count': result,  # Количество просмотренных уроков от всех учеников
                'all_time': sum_time,  # Сумма времени просмотров всех учеников
                'users': all_users,  # Количество учеников занимающихся на продукте
                'percent': percent,  # Процент приобретения продукта
            })
        return Response(statistic)
