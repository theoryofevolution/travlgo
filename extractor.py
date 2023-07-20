import json
import availability 
from datetime import datetime, timedelta
def get_days_between_dates(start_date, end_date):
    dates = []
    current_date = start_date + timedelta(days=1)
    while current_date < end_date: 
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates

def get_date_without_time(datetime_string):
    datetime_object = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
    date_without_time = datetime_object.strftime('%Y-%m-%d')
    return date_without_time


def extract_product_info(data, start_date, end_date):
    try:
        product_info = []
        #start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        #end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        for product in data.values():
            product_code = product['productCode']
            title = product['title']
            description = product['description']
            product_url = product['productUrl']
            duration = list(product['duration'].values())[-1]
            pricing_summary = product['pricing']['summary']
            from_price = pricing_summary['fromPrice']
            if 'reviews' in product:
                rating = list(product['reviews'].values())[2]
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

            date_range = get_days_between_dates(start_date, end_date)
            available = []
            for days in date_range:
                product_availability = availability.extract_available_times(product_code, str(days) )
                available.append(product_availability[0])
            product_info.append({
                    'productCode': product_code,
                    'title': title,
                    'description': description,
                    'productUrl': product_url,
                    'imageUrl': image_url,
                    'duration': duration,
                    'lengthType': length_type,
                    'rating': rating,
                    'price': from_price,
                    'availableOnDate': available,
                })
    except:
        pass
    return product_info