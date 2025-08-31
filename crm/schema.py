import graphene
from crm.models import Product  #  Product


# GraphQL type
class ProductType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    stock = graphene.Int()


#
class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # no  input

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10  # simulate restocking
            product.save()
            updated_products.append(product)

        return UpdateLowStockProducts(
            updated_products=updated_products,
            message="Low stock products updated successfully!"
        )


#
class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
