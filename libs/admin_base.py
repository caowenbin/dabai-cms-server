# coding: utf-8
from flask.ext.admin import Admin
from flask_admin._compat import as_unicode
from flask_admin.menu import MenuCategory, MenuView

__author__ = 'bin wen'


class Admin(Admin):
    """
        Collection of the admin views. Also manages menu structure.
    """
    def __init__(self, app=None, name=None,
                 url=None, subdomain=None,
                 index_view=None,
                 translations_path=None,
                 endpoint=None,
                 static_url_path=None,
                 base_template=None,
                 template_mode=None,
                 category_icon_classes=None):
        """
            Constructor.
        """
        self.app = app

        self.translations_path = translations_path

        self._views = []
        self._menu = []
        self._menu_categories = dict()
        self._menu_links = []

        if name is None:
            name = 'Admin'
        self.name = name

        self.static_url_path = static_url_path
        self.subdomain = subdomain
        self.base_template = base_template or 'admin/base.html'
        self.template_mode = template_mode or 'bootstrap2'
        self.category_icon_classes = category_icon_classes or dict()

        # Add predefined index view
        # self.add_view(self.index_view)

        # Register with application
        if app is not None:
            self._init_extension()

    def add_view(self, view):
        """
            Add a view to the collection.

            :param view:
                View to add.
        """
        # Add to views
        self._views.append(view)

        # If app was provided in constructor, register view with Flask app
        if self.app is not None:
            self.app.register_blueprint(view.create_blueprint(self))
        if view.is_menu:
            self._add_view_to_menu(view)

    def add_views(self, *args):
        """
            Add one or more views to the collection.

            Examples::

                admin.add_views(view1)
                admin.add_views(view1, view2, view3, view4)
                admin.add_views(*my_list)

            :param args:
                Argument list including the views to add.
        """
        for view in args:
            self.add_view(view)

    def add_link(self, link):
        """
            Add link to menu links collection.

            :param link:
                Link to add.
        """
        if link.category:
            self._add_menu_item(link, link.category)
        else:
            self._menu_links.append(link)

    def add_links(self, *args):
        """
            Add one or more links to the menu links collection.

            Examples::

                admin.add_links(link1)
                admin.add_links(link1, link2, link3, link4)
                admin.add_links(*my_list)

            :param args:
                Argument list including the links to add.
        """
        for link in args:
            self.add_link(link)

    def _add_menu_item(self, menu_item, target_category):
        if target_category:
            cat_text = as_unicode(target_category)

            category = self._menu_categories.get(cat_text)

            # create a new menu category if one does not exist already
            if category is None:
                category = MenuCategory(target_category)
                category.class_name = self.category_icon_classes.get(cat_text)
                self._menu_categories[cat_text] = category

                self._menu.append(category)

            category.add_child(menu_item)
        else:
            self._menu.append(menu_item)

    def _add_view_to_menu(self, view):
        """
            Add a view to the menu tree

            :param view:
                View to add
        """
        self._add_menu_item(MenuView(view.name, view), view.category)

    def get_category_menu_item(self, name):
        return self._menu_categories.get(name)

    def init_app(self, app):
        """
            Register all views with the Flask application.

            :param app:
                Flask application instance
        """
        self.app = app

        self._init_extension()

        # Register views
        for view in self._views:
            app.register_blueprint(view.create_blueprint(self))

    def _init_extension(self):
        if not hasattr(self.app, 'extensions'):
            self.app.extensions = dict()

        admins = self.app.extensions.get('admin', [])

        for p in admins:
            if p.endpoint == self.endpoint:
                raise Exception(u'Cannot have two Admin() instances with same'
                                u' endpoint name.')

            if p.url == self.url and p.subdomain == self.subdomain:
                raise Exception(u'Cannot assign two Admin() instances with same'
                                u' URL and subdomain to the same application.')

        admins.append(self)
        self.app.extensions['admin'] = admins

    def menu(self):
        """
            Return the menu hierarchy.
        """
        return self._menu

    def menu_links(self):
        """
            Return menu links.
        """
        return self._menu_links
