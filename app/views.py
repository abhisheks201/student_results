from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backend import EmailBackend

import jwt
from datetime import datetime, timedelta
from .serializers import UserSerializer,MarksSerializer
from .models import User,Marks

# from drf_yasg.utils import swagger_auto_schema

JWT_SECRET_KEY = 'project-insecure-6i9o@jxm94t!sao=x%*6yhx9fyht^62ir(wzw5sre^*a%lk02'
JWT_ACCESS_TOKEN_EXPIRATION = 60
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

logger = logging.getLogger('django')


def get_token_for_user(user):
    token_payload = {
        'user_id': str(user.id),
        'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRATION),
        'iat': datetime.utcnow()
    }
    access_token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM).decode('utf-8')

    refresh_token_payload = {
        'user_id': str(user.id),
        'exp': datetime.utcnow() + timedelta(days=JWT_REFRESH_TOKEN_EXPIRATION),
        'iat': datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM).decode('utf-8')
    return {
        'access': access_token,
        'refresh': refresh_token
    }

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# ...

class Register(APIView):
    @swagger_auto_schema(
        operation_description="User Registration",
        responses={200: "User created successfully"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['first_name', 'last_name', 'hall_ticket', 'gender', 'school', 'password'],
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'hall_ticket': openapi.Schema(type=openapi.TYPE_STRING),
                'gender': openapi.Schema(type=openapi.TYPE_STRING),
                'school': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
        ),
    )
    def post(self, request, format=None):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                password = serializer.validated_data['password']
                hashed_password = make_password(password)
                serializer.save(password=hashed_password)
                logger.info('User created successfully')
                return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            else:
                errors = serializer.errors
                logger.error("hall ticket already exists")  
                return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.warning("An exception occurred") 
            return JsonResponse({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="User Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'hall_ticket': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['hall_ticket', 'password'],
        ),
    )
    def post(self, request):
        try:
            hall_ticket = request.data.get('hall_ticket')
            password = request.data.get('password')

            if not hall_ticket or not password:
                logger.error('Missing required field(s): hall_ticket, password')
                return Response({'error': 'Missing required field(s): hall_ticket, password'},
                                status=status.HTTP_400_BAD_REQUEST)

            user = EmailBackend().authenticate(request, username=hall_ticket, password=password)
            if user is not None:
                token = get_token_for_user(user)
                logger.info("User successfully authenticated")
                return Response({
                    'status': 'success',
                    'msg': 'User successfully authenticated',
                    'token': token,
                    'user_id': str(user.id),
                })
            else:
                logger.warning('Invalid hall_ticket or password')
                return JsonResponse({'message': 'Invalid hall_ticket or password'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            logger.exception('An error occurred while processing the login request')
            return Response({'error': 'An error occurred while processing the login request'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def calculate_total_marks(mark):
    return (
        int(mark['telugu']) +
        int(mark['hindi']) +
        int(mark['english']) +
        int(mark['maths']) +
        int(mark['science']) +
        int(mark['social'])
    )

from .models import User

def add_additional_data(marks_data):
    serialized_data = []
    for mark in marks_data:
        total_marks = calculate_total_marks(mark)
        user_id = mark['user'] 
        user = User.objects.get(id=user_id)  
        hall_ticket = user.hall_ticket
        gender=user.gender
        name = user.first_name + ' ' + user.last_name
        data = {
            'hall_ticket': hall_ticket,
            'name': name,
            'gender':gender,
            'total_marks': total_marks,
            **mark  
        }
        serialized_data.append(data)
    return serialized_data



def get_data(request):
    try:
        if request.method == 'GET':
            marks = Marks.objects.all()
            serializer = MarksSerializer(marks, many=True)
            serialized_data = add_additional_data(serializer.data)
            logger.info("Retrieve the All data")
            return JsonResponse(serialized_data, safe=False)
        else:
            logger.error("Invalid request method")
            return JsonResponse({'error': 'Invalid request method'}, status=405)
    except Exception as e:
        logger.warning("An exception occurred: %s", str(e))
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

    

class MarksDetailView(APIView):
    def get(self, request, hall_ticket, format=None):
        password = request.query_params.get('password', None)

        try:
            user = User.objects.get(hall_ticket=hall_ticket)
        except User.DoesNotExist:
            logger.error('User not found: %s', hall_ticket)
            return JsonResponse({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            marks = Marks.objects.filter(user=user)
            serializer = MarksSerializer(marks, many=True)
            serialized_data = add_additional_data(serializer.data)
            logger.info("Retrieve the hall_ticket based data")
            return JsonResponse(serialized_data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('An error occurred while retrieving marks: %s', str(e))
            return JsonResponse({'message': 'Error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                   



class HighestMarksView(APIView):
    def get(self, request):
        try:
            highest_marks = Marks.objects.order_by('-telugu', '-hindi', '-english', '-maths', '-science', '-social').first()

            if highest_marks is not None:
                serializer = MarksSerializer(highest_marks)
                serialized_data = add_additional_data([serializer.data])
                logger.info("Retrieve the Highest marks data")
                return Response(serialized_data)
            else:
                return Response({'message': 'No marks data found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.warning('An error occurred while fetching highest marks')
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class RankAPI(APIView):
    def get(self, request):
        try:
            marks = Marks.objects.all().order_by(
                '-telugu', '-hindi', '-english', '-maths', '-science', '-social'
            )

            serializer = MarksSerializer(marks, many=True)
            serialized_data = add_additional_data(serializer.data)

            user_data = []
            for rank, mark in enumerate(serialized_data, start=1):
                user_data.append({
                    'rank': rank,
                    'user_id': mark['user'],
                    'name': mark['name'],
                    'total_marks': mark['total_marks']
                })
            logger.info("Get the data based on the Rank wise")
            return Response(user_data)

        except Exception as e:
            logger.warning("An error occurred while processing the request: %s", str(e))
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GenderMarksAPIView(APIView):

    def get(self, request, gender):
        try:
            marks = Marks.objects.filter(user__gender=gender)
            serializer = MarksSerializer(marks, many=True)

            data = []
            for mark, serialized_mark in zip(marks, serializer.data):
                user = mark.user
                total_marks = sum([int(mark.telugu), int(mark.hindi), int(mark.english),
                                   int(mark.maths), int(mark.science), int(mark.social)])

                mark_data = {
                    'hall_ticket': user.hall_ticket,
                    'name': f"{user.first_name} {user.last_name}",
                    'total_marks': total_marks,
                    'marks': serialized_mark,
                }
                data.append(mark_data)
            logger.info("Get the Data Based on M/F")
            return Response(data)

        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    