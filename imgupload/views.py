from typing import Annotated, List, final
from xmlrpc.server import DocXMLRPCRequestHandler
from django.http import Http404,HttpResponse
from django.shortcuts import redirect,render
from numpy import save
from imgupload.forms import UploadForm
from imgupload.models import FeedTable, ImageTable
import base64
from google.cloud import vision
from itertools import repeat, chain
import os
import json
from google.cloud.vision_v1 import AnnotateImageResponse


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"smartifydemo-b053ae69e5a1.json"



def home(request):
    return HttpResponse("ok")



def image(request,image_id):
    image=ImageTable.objects.get(pk=image_id)

    if image is not None:

        return render(request,'ocr/image.html',{'image':image})
    else:
        raise Http404('Error')




def text(request,text_id):
    text=FeedTable.objects.get(pk=text_id)

    if text is not None:

        return render(request,'ocr/text.html',{'text':text})
    else:
        raise Http404('Error')




def upload(request):

    if request.POST:

        
        form=UploadForm(request.POST,request.FILES)
        print(request.FILES)
        if form.is_valid():
            instance=form.save()
            print('obj',instance)
            print('obj',instance.id)
            image = instance.image
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
            client = vision.ImageAnnotatorClient()
            image= vision.Image(content=image_base64)
            response = client.text_detection(image=image)
            texts = response.full_text_annotation
            

            items = []
            lines = {}
            
    
        def lines_format():


            for text in response.text_annotations[1:]:
                top_x_axis = text.bounding_poly.vertices[0].x
                top_y_axis = text.bounding_poly.vertices[0].y
                bottom_y_axis = text.bounding_poly.vertices[3].y

                if top_y_axis not in lines:
                    lines[top_y_axis] = [(top_y_axis, bottom_y_axis), []]

                for s_top_y_axis, s_item in lines.items():
                    if top_y_axis < s_item[0][1]:
                        lines[s_top_y_axis][1].append(text.description)
                        break

            
            
            listoflines=[]

            for _, item in lines.items():
                list2 = filter(None, item[1])
                listToStr = ' '.join(map(str, list2))
                for _ in listToStr:
                    my_string = listToStr.strip()
                    listoflines.append(my_string)
                    text='\n'.join(listoflines)
                    break
            return text



        final_text=lines_format()
        create_new_record=FeedTable.objects.create(image_table_id=instance.id,text=final_text)
        create_new_record.save()              
       
        return redirect(home)

    return render(request, 'ocr/upload.html', {'form':UploadForm} )



    


def database(request):
    data=FeedTable.objects.all()
    return render(request,'ocr/database.html',{'data':data})
        
