from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# GET POST /category
# GET PUT DELETE /category


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class Categories(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        # DATA -> JSON
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        # JSON -> DATA
        if serializer.is_valid():
            new_catecory = serializer.save()
            # create 함수 실행
            # new_category 변수에는 새로 저장된 값이 담김
            return Response(
                CategorySerializer(new_catecory).data,
            )
        else:
            return Response(serializer.errors)


# @api_view(["GET", "POST"])
# def categories(request):
#     if request.method == "GET":
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         # DATA -> JSON
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = CategorySerializer(data=request.data)
#         # JSON -> DATA
#         if serializer.is_valid():
#             new_catecory = serializer.save()
#             # create 함수 실행
#             # new_category 변수에는 새로 저장된 값이 담김
#             return Response(
#                 CategorySerializer(new_catecory).data,
#             )
#         else:
#             return Response(serializer.errors)

# many True = 여러 속성들을 보낸다.
# return Response(CategorySerializer(Category.objects.all(), many=True).data)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,  # 데이터가 완전하지 않을수도 있다
            partial=True,  # 데이터가 완전하지 않을수도 있다
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        # return Response(status=204)
        return Response(status=HTTP_204_NO_CONTENT)


# @api_view(["GET", "PUT", "DELETE"])
# def category(request, category_id):
#     # id is coming from URL
#     try:
#         category = Category.objects.get(id=category_id)
#     except Category.DoesNotExist:
#         raise NotFound

#     if request.method == "GET":
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = CategorySerializer(
#             category,
#             data=request.data,  # 데이터가 완전하지 않을수도 있다
#             partial=True,  # 데이터가 완전하지 않을수도 있다
#         )
#         if serializer.is_valid():
#             updated_category = serializer.save()
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.errors)
#     elif request.method == "DELETE":
#         category.delete()
#         # return Response(status=204)
#         return Response(status=HTTP_204_NO_CONTENT)
