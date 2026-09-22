from adrf.views import APIView  
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from app.crud.price_history import get_price_history
from app.services.checker import process_tracking_checking
from app.crud.tracking import (
    create_tracking,
    delete_tracking,
    get_all_active_trackings,
    get_user_active_trackings,
    toggle_tracking_active
)
from app.db.session import AsyncSessionLocal
from .serializers import TrackingCreateSerializer, TrackingSerializer
from app.services.notifier import send_tg_notification
from .authentication import TelegramAuthentication


class TrackingListView(APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        user_id = int(request.user.telegram_id)
        async with AsyncSessionLocal() as session:
            trackings = await get_user_active_trackings(session, user_id=user_id)

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
                        text=   f"<b>I found cheap tickets for you right now!</b>\n\n"
                                f"Route: {new_tracking.origin_name} ➔ {new_tracking.destination_name}\n"
                                f"Date: {new_tracking.departure_date}\n"
                                f"Current price: <b>{current_price} ₸</b>\n"
                                f"Your target: {new_tracking.target_price} ₸",
                    )
                else: 
                    await send_tg_notification(
                                            chat_id=request.user.telegram_id, 
                                            text=   f"Current minimum price right now is <b>{current_price} ₸</b>.\n"
                                            f"We will notify you when price drops to or below {new_tracking.target_price} ₸.")
            else:
                await send_tg_notification(
                    chat_id=request.user.telegram_id,
                    text='Could not find active tickets for these parameters at the moment'
                )
                await session.commit()
                await session.refresh(new_tracking)

        output_serializer = TrackingSerializer(new_tracking)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

class TrackingDetailView(APIView):
    authentication_classes = [TelegramAuthentication]

    async def delete(self, request, pk):
        user_id = request.user.telegram_id
        
        try:
            tracking_id = int(pk)
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Invalid tracking ID'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        async with AsyncSessionLocal() as session:
            deleted = await delete_tracking(
                session=session,
                tracking_id=tracking_id,
                user_id=user_id,
            )

        if not deleted:
            return Response(
                {'detail': 'Tracking not found or not owned by user'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
    async def patch(self, request, pk):
        user_id  = request.user.telegram_id
        print(f"Client requesting tracking_id={pk} for user_id={user_id}")
        is_active = request.data.get('is_active')
        if is_active is None:
            return Response(
                {'detail': 'Field "is_active" is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        async with AsyncSessionLocal() as session:
            paused = await toggle_tracking_active(
                session=session,
                tracking_id=pk,
                user_id=user_id,
                is_active=is_active
            )
        if not paused:
            return Response(
                {'detail': 'Tracking not found or not owned by user'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = TrackingSerializer(paused)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PriceHistoryView(APIView):
    authentication_classes = [TelegramAuthentication]

    async def get(self, request, pk):
        async with AsyncSessionLocal() as session:
            history = await get_price_history(session, tracking_id=int(pk))
        
        data = [
            {
                "time": record.time.isoformat(),
                "price": float(record.price),
                "carrier": record.carrier
            }
            for record in history
        ]
        
        return Response(data) 