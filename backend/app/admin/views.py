from typing import Any

from sqladmin import ModelView

from backend.app.db.models import Profile, Product, CarBrand, CarModel, CarGen, DetailCategory, DetailType, CarInGarage

from wtforms.validators import Optional


class BaseAdminView(ModelView):
    form_include_pk = True
    form_excluded_columns = ['id', 'created_at']

    @property
    def column_list(self):
        return self.model.__table__.columns

    @property
    def form_args(self) -> dict[str, Any]:
        return {
            c.name: dict(validators=[Optional()])
            for c in self.model.__table__.columns
            if c.default or c.server_default
        }


class ProfileAdminView(BaseAdminView, model=Profile):
    pass


class ProductAdminView(BaseAdminView, model=Product):
    pass


class CarBrandAdminView(BaseAdminView, model=CarBrand):
    pass


class CarModelAdminView(BaseAdminView, model=CarModel):
    pass


class CarGenAdminView(BaseAdminView, model=CarGen):
    pass


class DetailCategoryAdminView(BaseAdminView, model=DetailCategory):
    pass


class DetailTypeAdminView(BaseAdminView, model=DetailType):
    pass


class CarInGarageAdminView(BaseAdminView, model=CarInGarage):
    pass


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
