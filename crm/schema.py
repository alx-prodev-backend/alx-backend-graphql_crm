import graphene
from graphene_django.types import DjangoObjectType
from .models import Product
from django.utils import timezone

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No args, it just auto-restocks

    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated = []
        for product in low_stock_products:
            product.stock += 10  # simulate restocking
            product.save()
            updated.append(product)

        if updated:
            msg = f"{len(updated)} products restocked at {timezone.now()}."
        else:
            msg = "No products needed restocking."

        return UpdateLowStockProducts(
            success=True,
            message=msg,
            updated_products=updated,
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
