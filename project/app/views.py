from rest_framework import serializers, viewsets
import datetime
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django_restful_admin import RestFulModelAdmin
from rest_framework.response import Response
from app.models import HoDan, CuuHo


class CuuHoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuuHo
        fields = '__all__'


class CuuHoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CuuHoSerializer
    queryset = CuuHo.objects.all()


class BaseRestfulAdmin(RestFulModelAdmin):
    permission_classes = ()


class HoDanRestFulModelAdmin(BaseRestfulAdmin):

    def list(self, request):
        ten = request.GET.get("ten")
        phone = request.GET.get("phone")
        tinh = request.GET.get("tinh")
        huyen = request.GET.get("huyen")
        xa = request.GET.get("xa")
        status = request.GET.get("status")
        fromTime = request.GET.get("from")
        toTime = request.GET.get("to")

        if phone or tinh or huyen or status or fromTime or toTime or ten:
            filter = Q()
            if ten:
                operator = request.GET.get("ten_method")
                if operator == "contain":
                    filter = filter & Q(name__icontains=ten)
                else:
                    filter = filter & Q(name__iexact=ten)
            if phone:
                filter = filter & Q(phone=phone)
            if tinh:
                filter = filter & Q(tinh=tinh)
            if huyen:
                filter = filter & Q(huyen=huyen)
            if xa:
                filter = filter & Q(xa=xa)
            if status:
                filter = filter & Q(status=status)
            if fromTime and toTime:
                start = datetime.datetime.strptime(
                    fromTime, "%Y-%m-%d-%H-%M-%S")
                end = datetime.datetime.strptime(toTime, "%Y-%m-%d-%H-%M-%S")
                filter = filter & Q(update_time__range=(start, end))

            queryset = HoDan.objects.filter(filter)
        else:
            # all if no filter
            queryset = HoDan.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
