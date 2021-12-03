import os, django, csv

# 카테고리 데이터 넣는 파일
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zara.settings')
django.setup()

from users.models import *
from products.models import *
from orders.models import *

csv_path = './csv/category.csv'
# csv_path = './csv/product.csv'
# csv_path = './csv/theme.csv'
# csv_path = './csv/theme_product.csv'
# csv_path = './csv/material.csv' # name,product,caution
# csv_path_size = './csv/size.csv' # name
# # csv_path_color = './csv/color.csv' # name, information 
# csv_path_product_option = './csv/product_option.csv' # sales,product_option,thumbnail_image_url,size,color,product
# csv_path_product_image = './csv/product_image.csv' # product,alt,url
# csv_path_user = './csv/user.csv' # sales,product_option,thumbnail_image_url,size,color,product
# csv_path_address = './csv/address.csv' # product,alt,url


with open(csv_path) as f:
    data_reader = csv.reader(f)
    next(data_reader, None)
    for row in data_reader:
        Category.objects.create(
            name = row[0],
            description = row[1],
            image_url = row[2]
        )

# product
# with open(csv_path) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Product.objects.create(
#             name = row[0],
#             price = row[1],
#             information = row[2],
#             category = Category.objects.get(name=row[3])
#         )

# # theme
# with open(csv_path) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Theme.objects.create(
# #             name = row[0]
#         )


# # theme_product
# with open(csv_path) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         ThemeProduct.objects.create(
#             product = Product.objects.get(name=row[0]),
#             theme = Theme.objects.get(name=row[1])
#         )


# # theme_product
# with open(csv_path) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Material.objects.create(
#             name = row[0],
#             caution = row[2]
#         )


# # Size
# with open(csv_path_size) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Size.objects.create(
#             name = row[0],
#             information = row[1]
#         )


# # Color
# with open(csv_path_color) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Color.objects.create(
#             name = row[0]
#         )
# product_option
# with open(csv_path_product_option) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         ProductOption.objects.create(
#             sales = row[0],
#             stock = row[1],
#             thumbnail_image_url = row[2],
#             size = Size.objects.get(name=row[3]),
#             color = Color.objects.get(name=row[4]),
#             product = Product.objects.get(name=row[5])
#         )

# csv_path_product_option = './csv/product_option.csv' # sales,product_option,thumbnail_image_url,size,color,product

# product_image
# with open(csv_path_product_image) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         ProductImage.objects.create(
#             product = Product.objects.get(name=row[0]),
#             alt = row[1],
#             url = row[2]
#         )

# csv_path_product_image = './csv/product_image.csv' # product,alt,url

#  User
# with open(csv_path_user) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         User.objects.create(
#             name = row[0],
#             email = row[1],
#             password = row[2],
#             phone = row[3],
#             cash = row[4]
#         )

# # csv_path_user = './csv/user.csv' #name,email,password,phone,cash

# # Address
# with open(csv_path_address) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Address.objects.create(
#             receiver = row[0],
#             address = row[1],
#             zipcode = row[2],
#             user = User.objects.get(name=row[3])
#         )

# # csv_path_address = './csv/address.csv' # receiver,address,zipcode,user