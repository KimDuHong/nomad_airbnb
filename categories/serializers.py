from rest_framework import serializers
from .models import Category


# class CategorySerializer(serializers.Serializer):

#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(
#         required=True,
#         max_length=50,
#     )
#     kind = serializers.ChoiceField(
#         choices=Category.CategoryKindChoices.choices,
#     )
#     created_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return Category.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         # instance = Category
#         instance.name = validated_data.get("name", instance.name)
#         # 앞의 파라미터를 get 하고 실패 시 뒤에 값으로 설정
#         instance.kind = validated_data.get("kind", instance.kind)
#         instance.save()
#         return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
