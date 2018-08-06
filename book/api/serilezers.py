from rest_framework.serializers import ModelSerializer
from book import models


class BookListSerializer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'

class BookDetailSerialzer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class BookDeleteSerialzer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class BookUpdateSerialzer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class BookCreateSerialzer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class BookManageSerialzer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'