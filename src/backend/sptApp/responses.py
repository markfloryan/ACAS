from rest_framework import viewsets, status
from rest_framework.response import Response

# ERROR Response

def unauthorized_access_response():
    return Response({
        'status': '400 - Bad Request',
        'result': 'You are either not logged in or not authorized to view this content'
    }, status=status.HTTP_400_BAD_REQUEST)

def no_implementation_response():
    return Response({
        'status': '400 - Bad Request',
        'result': 'This functionality is not implemented yet.'
    }, status=status.HTTP_400_BAD_REQUEST)

def id_token_error_response():
    return Response({
        'status': '404 - Not Found',
        'result': 'There appears to be a problem with your id_token'
    }, status=status.HTTP_404_NOT_FOUND)

def missing_id_response():
    return Response({
        'status': '400 - Bad Request',
        'result': 'Please specify ID to delete an object'
    }, status=status.HTTP_400_BAD_REQUEST)


def malformed_request_response(fields={}):
    # fields = str(fields)
    return Response({
        'status': '400 - Bad Request',
        "missing_data": fields
    }, status=status.HTTP_400_BAD_REQUEST)


def object_not_found_response():
    return Response({
        'status': '404 - Not Found',
        'result': 'Object with given id does not exist'
    }, status=status.HTTP_404_NOT_FOUND)

# Usually used for deletes, it means that other objects depend upon this one so you can't just delete it


def object_is_foreign_key_response():
    return Response({
        'status': '400 - Bad Request',
        'result': 'Object is a foreign key to other models and thus cannot be deleted'
    }, status=status.HTTP_409_CONFLICT)

# This means that data provided for an action is somehow invalid


def invalid_serializer_response(errors={}):
    return Response({
        'status': '400 - Bad Request',
        'missing data': errors
    }, status=status.HTTP_400_BAD_REQUEST)

# This means that the request can't be invoked on an existing object,
# for example trying to create an object where one already exists


def colliding_id_response(errors={}):
    return Response({
        'status': '400 - Bad Request',
        'result': 'Cannot POST data to an already created id'
    }, status=status.HTTP_400_BAD_REQUEST)


# This means that the total weight for a category was over 1 when trying to add a new category
def bad_weight_response(errors={}):
    return Response({
        'status': '400 - Bad Request',
        'result': 'Cannot POST data: Weight value over limit'
    }, status=status.HTTP_409_CONFLICT)

# This means that an error was recieved by Google or another external site
def external_error():
    return Response(data={
        'status': '400 - Bad Request',
        'result': 'Error with external request'
    }, status=status.HTTP_400_BAD_REQUEST)



# SUCCESS RESPONSES
def successful_delete_response():
    return Response({
        'status': '200 - No Content',
        'result': "Successfully deleted object"
    }, status=status.HTTP_200_OK)


def successful_get_externalSite():
    return Response({
        'status': '200 - OK',
        'result': {"Successfully retrieved external information"},
    }, status=status.HTTP_200_OK)

def successful_get_externalSite_withData(data): # pragma: no cover
    return Response({
        'status': '200 - OK',
        'result': data,
    }, status=status.HTTP_200_OK)

def successful_edit_response(data):
    return Response({
        'status': '200 - OK',
        'result': data
    }, status=status.HTTP_200_OK)


def successful_create_response(data):
    return Response({
        'status': '200 - OK',
        'result': data
    }, status=status.HTTP_200_OK)

def successful_submission_response(data):
    return Response({
        'status': '200 - OK',
        'result': data
    }, status=status.HTTP_200_OK)

def conflict_response(data):
    return Response({
        'status': '409 - Conflict',
        'result': data
    }, status=status.HTTP_409_CONFLICT)

def forbidden_response(data):
    return Response({
        'status': '403 - Forbidden',
        'result': data
    }, status=status.HTTP_403_FORBIDDEN)

def already_found_response():
    return Response({
        'status': '200 - OK'
    }, status=status.HTTP_200_OK)

def user_not_found_response():
    return Response({
        'status': '404 - Not Found',
        'result': 'Account does not exist'
    }, status=status.HTTP_404_NOT_FOUND)
