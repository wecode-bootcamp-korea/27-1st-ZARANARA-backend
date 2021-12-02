import os, django, csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE','zara.settings')
django.setup()

from users.models import *
from products.models import *
from orders.models import * 

# CATEGORY_PATH = './csv/category.csv'

# with open(CATEGORY_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Category.objects.create(
#             name = row[0],
#             description = row[1],
#             image_url = row[2]
#         )

# PRODUCT_PATH = './csv/product.csv'

# with open(PRODUCT_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Product.objects.create(
#             name = row[0],
#             price = row[1],
#             information = row[2],
#             category = Category.objects.get(name=row[3])
#         )

# THEME_PATH = './csv/theme.csv'

# with open(THEME_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Theme.objects.create(
#             name = row[0]
#         )   

# THEMEPRODUCT_PATH = './csv/theme_product.csv'

# with open(THEMEPRODUCT_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         ThemeProduct.objects.create(
#             product = Product.objects.get(name=row[0]),
#             theme = Theme.objects.get(name=row[1])
#         )

# manytomany 데이터 id 값 넣기 아직 안넣음

# MATERIAL_PATH = './csv/material.csv'

# with open(MATERIAL_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Material.objects.create(
#             name = row[0],
#             caution = row[2]
#         )

# PRODUCTSIMAGE_PATH = './csv/product_image.csv'

# with open(PRODUCTSIMAGE_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         ProductImage.objects.create(
#             product = Product.objects.get(name=row[0]),
#             alt = row[1],
#             url = row[2]
#         )

# SIZE_PATH = './csv/size.csv'

# with open(SIZE_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Size.objects.create(
#             name = row[0],
#             information = row[1]
#         )

# COLOR_PATH = './csv/color.csv'

# with open(COLOR_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Color.objects.create(
#             name = row[0]
#         )

# PRODUCTOPTION_PATH = './csv/product_option.csv'

# with open(PRODUCTOPTION_PATH) as f:
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

# User_PATH = './csv/user.csv'

# with open(User_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         User.objects.create(
#             name = row[0],
#             email = row[1],
#             password = row[2],
#             phone = row[3],
#             cash = row[4],
#         )

# User_PATH = './csv/user.csv'

# with open(User_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         User.objects.create(
#             name = row[0],
#             email = row[1],
#             password = row[2],
#             phone = row[3],
#             cash = row[4],
#         )

# ADDRESS_PATH = './csv/address.csv'

# with open(ADDRESS_PATH) as f:
#     data_reader = csv.reader(f)
#     next(data_reader, None)
#     for row in data_reader:
#         Address.objects.create(
#             receiver = row[0],
#             address = row[1],
#             zipcode = row[2],
#             user = User.objects.get(name=row[3])
#         )
