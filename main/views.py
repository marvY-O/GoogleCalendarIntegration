from django.http import HttpResponse
from django.shortcuts import render
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.conf import settings

# Create your views here.
def GoogleCalendarInitView(request):
    flow = Flow.from_client_config(
        {
            'web': {
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uris': ['http://localhost:8000/rest/v1/calendar/redirect/'],
                'auth_uri': settings.GOOGLE_AUTH_URI,
                'token_uri': settings.GOOGLE_TOKEN,
                'auth_provider_x509_cert_url': settings.GOOGLE_AUTH_PROVIDER_CERT_URL,
            }
        },
        state='your_state',
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['oauth_state'] = state

    return redirect(authorization_url)


def GoogleCalendarRedirectView(request):
    state = request.session.pop('oauth_state', '')
    if state != request.GET.get('state', ''):
        pass

    flow = Flow.from_client_config(
        {
            'web': {
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uris': ['http://localhost:8000/rest/v1/calendar/redirect/'],
                'auth_uri': settings.GOOGLE_AUTH_URI,
                'token_uri': settings.GOOGLE_TOKEN,
                'auth_provider_x509_cert_url': settings.GOOGLE_AUTH_PROVIDER_CERT_URL,
                # 'scopes': ['https://www.googleapis.com/auth/calendar.events.readonly'],
            }
        },
        state=state,
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    if credentials.expired:
        credentials.refresh(Request())

    service = build('calendar', 'v3', credentials=credentials)

    events = service.events().list(calendarId='primary').execute()

    return HttpResponse("Calendar events retrieved successfully!")