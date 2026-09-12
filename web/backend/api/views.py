from adrf.views import APIView  
from rest_framework import status
from rest_framework.response import Response

from app.crud.tracking import (
    create_tracking,
    deactivate_tracking,
    get_all_active_trackings,
)
from app.db.session import AsyncSessionLocal
from .serializers import TrackingCreateSerializer, TrackingSerializer


class TrackingListView(APIView):

    async def get(self, request):
        async with AsyncSessionLocal() as session:
            trackings = await get_all_active_trackings(session)

        serializer = TrackingSerializer(trackings, many=True)
        return Response(serializer.data)

    async def post(self, request):
        serializer = TrackingCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        async with AsyncSessionLocal() as session:
            new_tracking = await create_tracking(session, **validated_data)

        output_serializer = TrackingSerializer(new_tracking)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class TrackingDetailView(APIView):

    async def delete(self, request, pk):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        async with AsyncSessionLocal() as session:
            deactivated = await deactivate_tracking(
                session=session,
                tracking_id=pk,
                user_id=int(user_id)
            )

        if not deactivated:
            return Response(
                {'detail': 'Tracking not found or not owned by user.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)