from asgiref.sync import async_to_sync
from rest_framework.response import Response
from rest_framework.views import APIView
from app.crud.tracking import get_all_active_trackings
from app.db.session import AsyncSessionLocal

class TrackingListView(APIView):

  def get(self, request):
    async def fetch_data():
      async with AsyncSessionLocal() as db:
    
        return await get_all_active_trackings(db)

    trackings = async_to_sync(fetch_data)()

    result = [
        {
            "id": t.id,
            "user_id": t.user_id,
            "origin_name": t.origin_name,
            "destination_name": t.destination_name,
            "departure_date": str(t.departure_date),
        }
        for t in trackings
    ]
    return Response(result)