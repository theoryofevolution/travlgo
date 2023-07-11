import json

def extract_product_info(data):
    product_info = []
    
    for product in data.values():
        length_type = None
        product_code = product['productCode']
        title = product['title']
        description = product['description']
        product_url = product['productUrl']
        duration = product["duration"]["fixedDurationInMinutes"]
        if duration > 240:
            length_type = 'Full Day'
        elif 180 < duration <= 240:
            length_type = 'Half Day'
        elif duration <= 180:
            length_type = 'Part Day'
        image_url = None
        for image in product['images']:
            for variant in image['variants']:
                if variant['height'] == 160 and variant['width'] == 240:
                    image_url = variant['url']
                    break
            if image_url:
                break
        
        product_info.append({
            'productCode': product_code,
            'title': title,
            'description': description,
            'productUrl': product_url,
            'imageUrl': image_url,
            'duration': duration,
            'lengthType': length_type
        })
    
    return product_info