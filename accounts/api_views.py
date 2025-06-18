# accounts/api_views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
