from adrf.views import APIView  
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from app.services.checker import process_tracking_checking
from app.crud.tracking import (
    create_tracking,
    deactivate_tracking,
    get_all_active_trackings,
)
from app.db.session import AsyncSessionLocal
from .serializers import TrackingCreateSerializer, TrackingSerializer
from app.services.notifier import send_tg_notification
from .authentication import TelegramAuthentication


class TrackingListView(APIView):
    
    authentication_classes = [TelegramAuthentication]
    
    async def get(self, request):
        async with AsyncSessionLocal() as session:            
            trackings = await get_all_active_trackings(session)

        serializer = TrackingSerializer(trackings, many=True)
        return Response(serializer.data)

    async def post(self, request):
        serializer = TrackingCreateSerializer(data=request.data)
        if not serializer.is_valid():
            print("--- SERIALIZER ERRORS ---")
            print(serializer.errors)
            print("-------------------------")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        
        validated_data['user_id'] = request.user.telegram_id

        async with AsyncSessionLocal() as session:
            new_tracking = await create_tracking(session, **validated_data)
            
            should_notify, current_price = await process_tracking_checking(
                session=session, 
                tracking_info=new_tracking
            )
            
            print(f"DEBUG: current_price={current_price}, should_notify={should_notify}")
            
            if current_price is not None:
                new_tracking.price = current_price
                if should_notify:
                    await send_tg_notification(
                        chat_id=request.user.telegram_id, 
                        text='Tracking created!'
                    )
                await session.commit()
                await session.refresh(new_tracking)

        output_serializer = TrackingSerializer(new_tracking)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class TrackingDetailView(APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]

    async def delete(self, request, pk):
        user_id = request.user.telegram_id
        async with AsyncSessionLocal() as session:
            deactivated = await deactivate_tracking(
                session=session,
                tracking_id=pk,
                user_id=user_id
            )

        if not deactivated:
            return Response(
                {'detail': 'Tracking not found or not owned by user.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)