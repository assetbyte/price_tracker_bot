import pstats

from asgiref.sync import async_to_sync
from rest_framework.response import Response
from rest_framework.views import APIView
from app.crud.tracking import get_all_active_trackings, create_tracking, deactivate_tracking
from app.db.session import AsyncSessionLocal
from serializers import TrackingSerializer, TrackingCreateSerializer
from rest_framework import status

class TrackingListView(APIView):

  def get(self, request):
    async def fetch_data():
      async with AsyncSessionLocal() as db:
    
        return await get_all_active_trackings(db)

    trackings = async_to_sync(fetch_data)()

    serializer = TrackingSerializer(trackings, many=True)
    
    return Response(serializer.data)
  
  def post(self, request):
    serializer = TrackingCreateSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    
    async def create():
      async with AsyncSessionLocal() as session:
        new_tracking = await create_tracking(session, **validated_data)
        return new_tracking
    new_tracking = async_to_sync(create)()
    output_serializer = TrackingSerializer(new_tracking)
    return Response(output_serializer.data, status=status.HTTP_201_CREATED)
  
  
class TrackingDetailView(APIView):
  def delete(self, request, pk):
    user_id = request.query_params.get('user_id')
    if not user_id:
      return Response(
          {'error': 'user_id query parameter is required'},
          status=status.HTTP_400_BAD_REQUEST,
      )
      
    async def remove_tracking():
      async with AsyncSessionLocal() as session:
        return await deactivate_tracking(session=session, tracking_id=pk, user_id=int(user_id))
      
      deactivated = async_to_sync(remove_tracking)()
      
      if not is_deactivated:
        return Response(
          {'detail': 'Tracking not found or not owned by user.'},
          status=status.HTTP_404_NOT_FOUND,
      )

    return Response(status=status.HTTP_204_NO_CONTENT)
      
    
  
  
      