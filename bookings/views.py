from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Designer, Booking
from .serializers import DesignerSerializer, BookingSerializer
from users.permissions import IsStaffOrAbove

class CustomerBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # customer sees only their bookings
        bookings = Booking.objects.filter(customer=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageBookingsView(APIView):
    permission_classes = [IsStaffOrAbove]

    def get(self, request):
        # staff sees all bookings
        bookings = Booking.objects.all().order_by('-created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        booking.delete()
        return Response({'message': 'Booking deleted'})
class DesignerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        designers = Designer.objects.filter(is_available=True)
        serializer = DesignerSerializer(designers, many=True)
        return Response(serializer.data)


class DesignerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            designer = Designer.objects.get(pk=pk)
            serializer = DesignerSerializer(designer)
            return Response(serializer.data)
        except Designer.DoesNotExist:
            return Response(
                {'error': 'Designer not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class DesignerCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = DesignerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
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


class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(customer=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, customer=request.user)
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk,customer=request.user)
            serializer = BookingSerializer(booking, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
