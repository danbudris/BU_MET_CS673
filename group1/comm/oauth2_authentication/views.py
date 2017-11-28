import io
import httplib2
from oauth2client.client import flow_from_clientsecrets
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
from apiclient import discovery
from apiclient.http import MediaIoBaseDownload


DOWNLOAD_REDIRECT = 'http://localhost:8000/communication/oauth2/oauth2callback/filedownload'

DOWNLOAD_FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/drive',
    redirect_uri=DOWNLOAD_REDIRECT
)


@login_required
def file_download(request, file_id=None):
    DOWNLOAD_FLOW.params['state'] = file_id
    authorize_url = DOWNLOAD_FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)


@login_required
def callback_download(request):
    download_file_id = request.REQUEST['state']
    credential = DOWNLOAD_FLOW.step2_exchange(request.REQUEST)
    http = httplib2.Http()
    http = credential.authorize(http)
    service = discovery.build('drive', 'v3', http=http)
    # This hardcoded file name is only being used for testing.
    # In the future, the file name should be determined through the Google Drive API
    file_name = 'Project_Download_File_Test'
    request = service.files().export_media(fileId=download_file_id, mimeType='text/plain')
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download {}.".format(int(status.progress() * 100)))

    return HttpResponseRedirect("/communication")
