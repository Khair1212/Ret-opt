from .models import Product
from django.db.models import Case, When

recommendation_list = []
def recom(customer, ordered_products):
    for purchased in ordered_products:
        print(purchased.product.name) 
        if purchased.product.name == 'Mens Bag' : 
            r_id = [5, 14] 
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)]) 
            pds = Product.objects.filter(id__in=[5, 14]).order_by(r_ordering) 
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Woman Bag':
            r_id = [14, 5]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[14, 5]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Mens Shirt' :
            r_id = [0, 12, 21]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[0, 12, 21]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Far From The Tree - Books' :
            r_id = [1, 4, 7, 13 ,16, 22]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[1, 4, 7, 13 ,16, 22]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Nike Shoe' :
            r_id = [2, 8, 9]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[2, 9, 8]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Oneplus 8' :
            r_id = [3, 10, 11, 15, 19]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[3, 10, 11, 15, 19]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'War and Peace - Book' :
            r_id=[4, 7, 16, 13, 22, 1]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[4, 7, 16, 13, 22, 1]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Kitchen Accesories' :
            r_id = [6, 17, 18 , 20]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[6, 17, 18, 20]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'How Big Worries - Book' :
            r_id = [17, 20, 18, 6]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[17, 20, 18, 6]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Kids Shoe' :
            r_id = [8, 9, 2]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[8, 9, 2]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Woman Shoe' :
            r_id = [9, 8 , 2]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[9, 8, 2]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Sony Headset' :
            r_id = [15, 19, 10, 11, 3]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[15, 19, 10, 11, 3]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Philips Trimmer' :
            r_id = [11, 10, 15, 19, 3]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[11, 10, 15, 19, 3]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Kids Dress' :
            r_id = [12, 21, 0]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[12, 21, 0]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'English For Today - Book' :
            r_id = [4, 7, 13, 16, 22, 1]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[4, 7, 13, 16, 22, 1]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Dell Inspiron Laptop' :
            r_id = [11, 10, 19, 15, 3]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[11, 10, 19, 15, 3]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Book Case' :
            r_id = [13, 16, 4, 7, 1]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[13, 16, 4, 7, 1]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Kitchen Cabinet' :
            r_id = [18, 6, 20, 17]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[18, 6, 20, 17]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Kitchen Accesories' :
            r_id = [6, 20, 17, 18]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[6, 20, 17, 18]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'FujiFilm Camera':
            r_id = [11, 3, 15, 10, 19]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[11, 3, 15, 10, 19]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Kitchen Sink' : 
            r_id = [18, 17, 6, 20] 
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)]) 
            pds = Product.objects.filter(id__in=[18, 17, 6, 20]).order_by(r_ordering) 
            recommendation_list.extend(pds) 
        elif purchased.product.name == 'Woman Dress' :
            r_id = [21, 22, 0]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[21, 22, 0]).order_by(r_ordering)
            recommendation_list.extend(pds)
        elif purchased.product.name == 'Avengers - Book' :
            r_id = [22, 13, 16, 7, 4]
            r_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(r_id)])
            pds = Product.objects.filter(id__in=[22, 13, 16, 7, 4]).order_by(r_ordering)
            recommendation_list.extend(pds)

    
    
    male_ids = [2, 5, 3, 0, 10, 11, 15, 13]
    male_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(male_ids)])

    female_ids = [9, 21, 14, 20, 18, 8, 12, 22]
    female_ordering = Case(*[When(id=id, then=pos) for pos, id in enumerate(female_ids)])


    if customer.gender=='M':
        # pds = Product.objects.filter(id__in=[2, 5, 14, 3,0,  10, 11, 15])
        pds = Product.objects.filter(id__in=male_ids).order_by(male_ordering)
        print(pds)
        recommendation_list.extend(pds)    
    
    elif customer.gender=='F':
        pds = Product.objects.filter(id__in=female_ids).order_by(female_ordering)
        recommendation_list.extend(pds)

    
    return recommendation_list