from datetime import date
from typing import Any

from flask import Request
import functions_framework
from google.cloud.firestore import Client, CollectionReference, Query


@functions_framework.http
def get_diaries(request: Request) -> dict[str, Any]:
    month = request.args.get('month', date.today().strftime('%Y%m'))

    client = Client(project='ceshmina-shu-test')
    collection: CollectionReference = (client
        .collection('contents').document('diary')
        .collection('months').document(month)
        .collection('entries'))
    query = (collection
        .order_by('date', direction=Query.DESCENDING)
        .order_by('created_at', direction=Query.DESCENDING))
    
    data = [
        {'id': document.id, **document.to_dict()}
        for document in query.stream()
    ]
    return {'data': data}
