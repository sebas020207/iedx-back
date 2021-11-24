from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.forms.models import model_to_dict
from .serializers import UserSerializer, ChangePasswordSerializer
from .models import Administrator
from historical.models import History
import mimetypes
from base64 import b64decode, b64encode


# Create your views here.
class CreateUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        if not request.user.role:
            return HttpResponseForbidden("Unauthorized")

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        action = 'ADDED: '+request.data['name']
        history = History.objects.create(name=request.user.name, action=action)
        history.save()
        return Response(serializer.data)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def update_action(self, object_before, object_after):
        object_difference = {
            key: 'Before: '+str(object_before[key])+' After: '+str(object_after[key])+'. ' for key in object_before if object_before[key] != object_after[key]
        }
        if object_difference:
            action = 'UPDATE: '
            for key in object_difference:
                action += key.capitalize()+' '+object_difference[key]
            return action
        else:
            return False

    def get_object(self, pk):
        try:
            return Administrator.objects.get(pk=pk)
        except Administrator.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user.role:
            return HttpResponseForbidden("Unauthorized")

        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not request.user.role:
            return HttpResponseForbidden("Unauthorized")

        user = self.get_object(pk)
        object_before = model_to_dict(user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            object_after = model_to_dict(user)
            action = self.update_action(object_before, object_after)
            if action:
                history = History.objects.create(
                    name=request.user.name, action=action)
                history.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCountView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        active = Administrator.objects.filter(is_active=True)

        response = Response()

        response.data = {
            "users": len(active)
        }
        return response


class AllUsersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if not request.user.role:
            return HttpResponseForbidden("Unauthorized")
        query_params = request.query_params
        filters = {}
        a_to_z = 'name'
        filters['is_active'] = True
        if 'search_item' in query_params:
            filters['name__contains'] = query_params['search_item']
        if 'order_by' in query_params and query_params['order_by'] == 'z_a':
            a_to_z = '-' + a_to_z
        users = Administrator.objects.filter(**filters).order_by(a_to_z)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserImages(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Administrator.objects.get(pk=pk)
        except Administrator.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        try:
            image = user.photo
            return HttpResponse(user.photo, content_type="image/png")
        except:
            raise Http404

    # def get(self, request, pk, format=None):
    #     user = self.get_object(pk)
    #     try:
    #         value = user.photo
    #         mime_type, encoding = mimetypes.guess_type(str(value))
    #         if not mime_type:
    #             mime_type = 'image/png'
    #         data = value.file.read()
    #         image_data = bytes(
    #             'data:' + mime_type + ';base64,', encoding='UTF-8') + b64encode(data)
    #         return HttpResponse(image_data)  # or str(image_data, 'utf-8')
    #     except:
    #         raise Http404


class MyInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def update_action(self, object_before, object_after):
        object_difference = {
            key: 'Before: '+str(object_before[key])+' After: '+str(object_after[key]) for key in object_before if object_before[key] != object_after[key]
        }
        if object_difference:
            action = 'UPDATE:'
            for key in object_difference:
                action += key.capitalize()+' '+object_difference[key]
            return action
        else:
            return False

    def get(self, request):
        content = {
            "id": request.user.id,
            "email": request.user.email,
            "name": request.user.name,
            "last_name": request.user.last_name,
            "role": request.user.role,
            "phone": request.user.phone,
            "address": request.user.address,
        }
        return Response(content)

    def put(self, request):
        user = Administrator.objects.get(pk=request.user.id)
        object_before = model_to_dict(user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            object_after = model_to_dict(user)
            action = self.update_action(object_before, object_after)
            if action:
                history = History.objects.create(
                    name=request.user.name, action=action)
                history.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }
        return Response(response)

# class LoginView(APIView):
#     def post(self, request, format=None):
#         email = request.data['email']
#         password = request.data['password']

#         user = Administrator.objects.filter(email=email).first()

#         if user is None:
#             raise AuthenticationFailed('User not found!')

#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect email or password!')

#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }

#         token = jwt.encode(payload, 'secret',
#                            algorithm='HS256')

#         response = Response()

#         #response.set_cookie(key='jwt', value=token, httponly=True)
#         response.headers['token'] = token
#         response.data = {
#             'jwt': token
#         }
#         return response


# class LogoutView(APIView):
#     def post(self, request):
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data = {
#             'message': 'success'
#         }
#         return response
