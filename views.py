import requests
from django.http import JsonResponse

def buscar_imagenes_unsplash(request):
    if request.method == 'GET':
        # Término de búsqueda
        query = request.GET.get('query')

        # Clave de API de Unsplash
        access_key = 'pvB6Yil1Un63AYmTFxNNqbSaflJxnqGrzEqlC9GQJAY'

        # URL del endpoint del API
        url = 'https://api.unsplash.com/search/photos'

        # Parámetros de la solicitud
        params = {'query': query}

        # Encabezados de la solicitud con la clave de API
        headers = {'Authorization': f'Client-ID {access_key}'}

        # Realiza la solicitud al API de Unsplash
        response = requests.get(url, params=params, headers=headers)

        # Procesa la respuesta
        if response.status_code == 200:
            data = response.json()
            # Retorna los datos como una respuesta JSON
            return JsonResponse(data)
        else:
            # Si hay un error, retorna un mensaje de error
            return JsonResponse({'error': 'Error al obtener imágenes'}, status=response.status_code)