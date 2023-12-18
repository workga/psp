from sqladmin import ModelView

from backend.app.db.models import Profile, Product, CarBrand, CarModel, CarGen, DetailCategory, DetailType, CarInGarage


class BaseAdminView:
    form_include_pk = True
    form_excluded_columns = ['id', 'created_at']


class ProfileAdminView(BaseAdminView, ModelView, model=Profile):
    column_list = Profile.__table__.columns


class ProductAdminView(BaseAdminView, ModelView, model=Product):
    column_list = Product.__table__.columns


class CarBrandAdminView(BaseAdminView, ModelView, model=CarBrand):
    column_list = CarBrand.__table__.columns


class CarModelAdminView(BaseAdminView, ModelView, model=CarModel):
    column_list = CarModel.__table__.columns


class CarGenAdminView(BaseAdminView, ModelView, model=CarGen):
    column_list = CarGen.__table__.columns


class DetailCategoryAdminView(BaseAdminView, ModelView, model=DetailCategory):
    column_list = DetailCategory.__table__.columns


class DetailTypeAdminView(BaseAdminView, ModelView, model=DetailType):
    column_list = DetailType.__table__.columns


class CarInGarageAdminView(BaseAdminView, ModelView, model=CarInGarage):
    column_list = CarInGarage.__table__.columns


def get_view_classes() -> list[type]:
    return [
        ProfileAdminView,
        ProductAdminView,
        CarBrandAdminView,
        CarModelAdminView,
        CarGenAdminView,
        DetailCategoryAdminView,
        DetailTypeAdminView,
        CarInGarageAdminView,
    ]


def get_generated_view_classes() -> list[type]:
    views_classes = []
    for cls in (
        Profile,
        Product,
        CarBrand,
        CarModel,
        CarGen,
        DetailCategory,
        DetailType,
        CarInGarage
    ):
        class ModelAdminView(ModelView, model=cls):
            column_list = cls.__table__.columns

        ModelAdminView.__name__ = ModelAdminView.__qualname__ = f"{cls.__name__}GeneratedAdminView"

        views_classes.append(ModelAdminView)

    return views_classes
