def register_routes(app):

  # Light Show Controller
  from app.controllers.light_show_controller import create as light_show_create
  app.add_url_rule('/light_show', view_func=light_show_create, methods=['POST'])