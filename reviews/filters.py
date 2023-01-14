from django.contrib import admin


class WordFilter(admin.SimpleListFilter):
    title = "filter by payload"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


class RatingFilter(admin.SimpleListFilter):
    title = "sort by rating"
    parameter_name = "rating"

    def lookups(self, request: any, model_admin: any):
        return [
            ("bad", "Bad"),
            ("soso", "Soso"),
            ("great", "Great"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word == "bad":
            return reviews.filter(rating__lt=3)
        elif word == "soso":
            return reviews.filter(rating__exact=3)
        else:
            return reviews.filter(rating__gt=3)
