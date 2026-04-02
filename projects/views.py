from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.views import APIView
from .cost_estimation import estimate_cost

class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(customer=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, customer=request.user)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response(
                {'error': 'Project not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, customer=request.user)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Project.DoesNotExist:
            return Response(
                {'error': 'Project not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, customer=request.user)
            project.delete()
            return Response(
                {'message': 'Project deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Project.DoesNotExist:
            return Response(
                {'error': 'Project not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class CostEstimationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room_type = request.data.get('room_type')
        room_size_sqft = request.data.get('room_size_sqft')
        material_quality = request.data.get('material_quality')
        design_style = request.data.get('design_style')

        if not all([room_type, room_size_sqft, material_quality, design_style]):
            return Response(
                {'error': 'All fields are required'},
                status=400
            )

        cost = estimate_cost(
            room_type,
            float(room_size_sqft),
            material_quality,
            design_style
        )

        return Response({
            'room_type': room_type,
            'room_size_sqft': room_size_sqft,
            'material_quality': material_quality,
            'design_style': design_style,
            'estimated_cost': f"₹ {cost}"
        })