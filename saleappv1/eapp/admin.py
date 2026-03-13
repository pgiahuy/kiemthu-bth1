from tkinter.font import names

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from eapp.models import Category, Product, UserRole
from eapp import db, app
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect
import dao

class AdminView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ProductView(AdminView):
    column_list = ['id', 'name', 'price', 'active', 'category_id']
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'price']
    can_export = True
    edit_modal = True
    column_editable_list = ['name']
    page_size = 30


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html',
                           revenue_products=dao.revenue_by_product(),
                           revenue_times=dao.revenue_by_time("month"))

    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', cate_stats=dao.count_product_by_cate())


admin = Admin(app=app, name="e-Commerce's Admin", index_view=MyAdminIndexView())

admin.add_view(AdminView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
