from rest_framework.decorators import api_view, permission_classes
from data.models import CustomUser, Blog
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login, logout, authenticate


"""
API: all infomation user
"""
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def api_user_list(request):
    if request.method == "GET":
        try:
            list_users = CustomUser.objects.all()
            data = list(list_users.values())
            return Response({"message": "Success", "data": data}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "ERROR", "data": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "Denie"}, status=status.HTTP_400_BAD_REQUEST)


"""
API: user(id) , information user and update information user
"""
@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def api_user_info(request, pk):
    if request.method == "GET":
        try:
            user_info = CustomUser.objects.get(pk=pk)
            text = {
                "pk": user_info.pk,
                "username": user_info.username,
                "token": str(request.auth),
                "emai": user_info.email,
                "is_active": user_info.is_active,
            }
            return Response({"message": "success", "data": text}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "ERROR", "data": "NULL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == "POST":
        try:
            user_info = CustomUser.objects.get(pk=pk)
            if not user_info:
                return Response({"message": "account not found"}, status=status.HTTP_404_NOT_FOUND0)
            else:
                user_info.username = request.data.get('username', user_info.username)
                user_info.first_name = request.data.get('first_name', user_info.first_name)
                user_info.last_name = request.data.get('last_name', user_info.last_name)
                user_info.email = request.data.get('email', user_info.email)
                user_info.is_active = request.data.get('is_active', user_info.is_active)
                user_info.favorites = request.data.get('favorites', user_info.favorites)
                # text = {
                #     "pk": user_info.pk,
                #     "username": user_info.username,
                #     "token": str(request.auth),
                #     "emai": user_info.email,
                #     "is_active": user_info.is_active,
                # }
                user_info.save()
                return Response({"message": "success", "data": request.data}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "ERROR", "data": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "notfound"}, status=status.HTTP_404_NOT_FOUND)


"""
API: login
"""
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def api_login(request):
    if request.method == "POST":
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if (not username) or (not password):
            return Response({'message': 'Not input data'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = authenticate(username=username, password=password)
                print(type(user))
                if not user:
                    return Response({"message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    login(request, user)
                    return Response({"user": user.username, "message": "success"}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"message": "Server is busy"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "Denie", "data": "Not Authentication"}, status=status.HTTP_400_BAD_REQUEST)


"""
API: return list blog
"""
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def api_list_blog(request):
    if request.method == "GET":
        try:
            list_blog = Blog.objects.all()
            return Response({"message": "success", "data": list(list_blog.values())}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"message": "ERROR", "data": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "Denie", "data": ""}, status=status.HTTP_400_BAD_REQUEST)


"""
API: return one blog and update or delete blog.
"""
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def api_one_blog(request, id):
    if request.method == "GET":
        try:
            blog_info = Blog.objects.get(id=id)
            text = {
                "id": blog_info.id,
                "title": blog_info.title,
                "content": blog_info.content,
                "vote": blog_info.vote,
                "accountID": blog_info.accountID.username,
            }
            return Response({"message": "success", "data": text}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"message": "ERROR", "data": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "POST":
        try:
            blog_info = Blog.objects.get(id=id)
            blog_info.title = request.data.get('title', blog_info.title)
            blog_info.content = request.data.get('content', blog_info.content)
            blog_info.vote = request.data.get('vote', blog_info.vote)
            blog_info.save()
            return Response({"message": "success", "data": request.data}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"message": "ERROR", "data": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "DELETE":
        try:
            blog_info = Blog.objects.get(id=id)
            text = {
                "id": blog_info.id,
                "title": blog_info.title,
                "content": blog_info.content,
                "vote": blog_info.vote,
                "accountID": blog_info.accountID.username,
            }
            blog_info.delete()
            return Response({"message": "success", "data": text}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": "ERROR", "data": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "Denie", "data": ""}, status=status.HTTP_400_BAD_REQUEST)


"""
API: vote one blog
"""
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def api_one_blog_vote(request, id):
    if request.method == "GET":
        try:
            blog_info = Blog.objects.get(id=id)
            blog_info.vote = blog_info.vote + 1
            blog_info.save()
            text = {
                "id": blog_info.id,
                "title": blog_info.title,
                "content": blog_info.content,
                "vote": blog_info.vote,
                "accountID": blog_info.accountID.username
            }
            return Response({"message": "success", "data": text}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"message": "ERROR", "data": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
API: add new blog
"""
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def api_new_blog(request):
    if request.method == "POST":
        try:
            error = []
            title = request.data.get("title", "")
            content = request.data.get("content", "")
            if not title:
                error.append("title not found")
            if not content:
                error.append("content not found")
            if error:
                return Response({"message": "fail", "data": error}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    new_blog = Blog.objects.create(title=title, content=content, vote=0, accountID=request.user)
                    text = {
                        "id": new_blog.id,
                        "title": title,
                        "content": content,
                        "vote": new_blog.vote,
                        "accountID": request.user.id
                    }
                    return Response({"message": "success", "data": text}, status=status.HTTP_200_OK)
                except Blog.DoesNotExist:
                    return Response({"message": "fail", "data": "Server is busy"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Blog.DoesNotExist:
            return Response({"message": "ERROR", "data": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "Denie", "data": ""}, status=status.HTTP_400_BAD_REQUEST)