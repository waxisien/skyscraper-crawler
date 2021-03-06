from flask import Flask, Markup
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from skycrawler.model import Building, City
from skycrawler.database import db_session

app = Flask(__name__)
app.config.from_envvar('SKY_ADMIN_SETTINGS')


class BuildingView(ModelView):
    can_delete = False
    can_create = False
    column_searchable_list = ['name', 'city.name']

    def _link_formatter(view, context, model, name):
        if model.link:
            markupstring = "<a href='%s' target='_blank'>%s</a>" % (model.link, model.link)
            return Markup(markupstring)
        else:
            return ""

    column_formatters = {
        'link': _link_formatter
    }


class CityView(ModelView):
    can_delete = False
    can_create = False
    column_searchable_list = ['name']

admin = Admin(app, name='skycrawler', template_mode='bootstrap3')
admin.add_view(BuildingView(Building, db_session))
admin.add_view(CityView(City, db_session))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(debug=True)
