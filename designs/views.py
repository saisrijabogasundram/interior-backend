from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Design
from .serializers import DesignSerializer
from rest_framework.parsers import MultiPartParser, FormParser
class DesignListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category = request.query_params.get('category', None)
        style = request.query_params.get('style', None)
        budget = request.query_params.get('budget', None)

        designs = Design.objects.all()

        if category:
            designs = designs.filter(category=category)
        if style:
            designs = designs.filter(style=style)
        if budget:
            designs = designs.filter(budget=budget)

        serializer = DesignSerializer(designs, many=True,context={'request': request} )
        return Response(serializer.data)


class DesignDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            design = Design.objects.get(pk=pk)
            serializer = DesignSerializer(design)
            return Response(serializer.data)
        except Design.DoesNotExist:
            return Response(
                {'error': 'Design not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class DesignCreateView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        serializer = DesignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DesignUpdateDeleteView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    def put(self, request, pk):
        try:
            design = Design.objects.get(pk=pk)
            serializer = DesignSerializer(design, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Design.DoesNotExist:
            return Response(
                {'error': 'Design not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            design = Design.objects.get(pk=pk)
            design.delete()
            return Response(
                {'message': 'Design deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Design.DoesNotExist:
            return Response(
                {'error': 'Design not found'},
                status=status.HTTP_404_NOT_FOUND
            )