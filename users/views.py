import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from .models import User
from reviews.serializers import ReviewSerializer
from rooms.serializers import RoomListSerializer
from . import serializers
from django.conf import settings
from rest_framework.exceptions import ValidationError
import requests


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def validate_password(self, password):
        import re

        REGEX_PASSWORD = "^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$"
        if not re.fullmatch(REGEX_PASSWORD, password):
            raise ParseError(
                "비밀번호를 확인하세요. 최소 1개 이상의 소문자, 숫자, 특수문자로 구성되어야 하며 길이는 8자리 이상이어야 합니다."
            )

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Invalid password")

        # serializer 에서 password 여부 체크는 하지 않음.
        # 추가 validation을 view 쪽에서 처리

        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            password = str(password)
            self.validate_password(password)
            user = serializer.save()
            user.set_password(password)

            # user.password = password 시에는 raw password로 저장
            user.save()

            # set_password 후 다시 저장
            serializer = serializers.PrivateUserSerializer(user)
            login(request, user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PublicUserSerializer(user)
        return Response(serializer.data)


class PublicUserReviews(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        user = self.get_object(username)
        serializer = ReviewSerializer(
            user.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class PublicUserRooms(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        user = self.get_object(username)
        serializer = RoomListSerializer(
            user.rooms.all()[start:end],
            context={"request": request},
            many=True,
        )
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError("Invalid password")
        if user.check_password(old_password):
            print(user.check_password)
            user.set_password(new_password)
            user.save()
            return Response(status=200)
        else:
            return Response(status=400)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"LogOut": True})


class JWTLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("Invalid username or password")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"Error": "Wrong Passwrod"})


class GithubLogIn(APIView):
    def post(self, request):
        try:
            # <---post 시 담겨오는 토큰값을 받아오고 해당 값으로 post 요청 -->
            # <----------토큰 교체 --------->
            git_url = "https://github.com/login/oauth/access_token"
            code = "?code=" + request.data.get("code")
            client_id = "&client_id=34e6a768f8bfa936a0a6"
            client_secrect = f"&client_secret={settings.GH_SECRET}"
            access_token = (
                requests.post(
                    git_url + code + client_id + client_secrect,
                    headers={"Accept": "application/json"},
                )
                .json()
                .get("access_token")
            )
            # <---------- 받아온 토큰 값으로 유저 데이터를 요청 ------->
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            ).json()

            # 이메일이 3개가 들어옴 그중 첫번쨰

            user_email = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            ).json()[0]

            # 이메일이 같은 유저가 있으면 로그인, 혹은 회원가입

            try:
                user = User.objects.get(email=user_email.get("email"))
            except User.DoesNotExist:
                if user_data.get("name") == None:
                    user_name = user_data.get("login")
                else:
                    user_name = user_data.get("name")
                print(user_data)
                user = User.objects.create(
                    username=user_data.get("login"),
                    name=user_name,
                    avatar=user_data.get("avatar_url"),
                    email=user_email.get("email"),
                )
                # 깃허브 로그인 유저는 패스워드 사용 불가
                user.set_unusable_password()
                user.save()

            login(request, user)
            return Response(status=200)

        except Exception as e:
            print(e)
            return Response(status=400)


class KakaoLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = (
                requests.post(
                    "https://kauth.kakao.com/oauth/token",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data={
                        "grant_type": "authorization_code",
                        "client_id": "da7b6b984fe482fd404d22bff8e2f803",
                        "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                        "code": code,
                    },
                )
                .json()
                .get("access_token")
            )
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                },
            ).json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)
                return Response(status=200)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
            user.set_unusable_password()
            user.save()
            login(request, user)
            return Response(status=200)
        except Exception:
            return Response(status=400)
