from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def dummy_segmentation(image):
   
    segmented_image = image.convert("L")  
    area = (image.size[0] * image.size[1]) // 2
    return segmented_image, area

@api_view(['POST'])
@parser_classes([JSONParser])
def greet_view(request):
    name = request.data.get("name", "")
    if name:
        greeting = f"Hello, {name}! I am here responding from server"
        return JsonResponse({"message": greeting})
    return JsonResponse({"error": "Name not provided"}, status=400)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def segment_view(request):
    if 'image' not in request.FILES:
        return JsonResponse({"error": "No image provided"}, status=400)

    file_obj = request.FILES['image']
    image = Image.open(file_obj)


    segmented_image, area = dummy_segmentation(image)
    buffer = BytesIO()
    segmented_image.save(buffer, format="PNG")
    buffer.seek(0)
    segmented_image_file = InMemoryUploadedFile(buffer, None, 'segmented.png', 'image/png', buffer.tell(), None)
    segmented_image_str = buffer.getvalue().decode('latin-1')

    return JsonResponse({
        "segmented_image": segmented_image_str,
        "area": area
    })
