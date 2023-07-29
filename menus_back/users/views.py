from rest_framework import views, response
from rest_framework.authtoken.models import Token
from users.models import User


class TokensListView(views.APIView):

    def get(self, request, **kwargs):
        res = {}
        for user in User.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            res[user.username] = {
                'token': token.key
            }
        return response.Response(res)