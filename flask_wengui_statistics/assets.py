"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """Create stylesheet bundles."""
    assets.auto_build = True
    assets.debug = False
    # common_style_bundle = Bundle(
    #     "src/less/*.less",
    #     filters="less,cssmin",
    #     output="dist/css/style.css",
    #     extra={"rel": "stylesheet/less"},
    # )
    index_style_bundle = Bundle(
        "index_bp/less/*.less",
        filters="less,cssmin",
        output="dist/css/index.css",
        extra={"rel": "stylesheet/less"},
    )
    auth_style_bundle = Bundle(
        "auth_bp/less/*.less",
        filters="less,cssmin",
        output="dist/css/auth.css",
        extra={"rel": "stylesheet/less"},
    )
    # signup_style_bundle = Bundle(
    #     "signup_bp/less/*.less",
    #     filters="less,cssmin",
    #     output="dist/css/signup.css",
    #     extra={"rel": "stylesheet/less"},
    # )
    dashboard_style_bundle = Bundle(
        "dashboard_bp/less/*.less",
        filters="less,cssmin",
        output="dist/css/dashboard.css",
        extra={"rel": "stylesheet/less"},
    )
    # home_style_bundle = Bundle(
    #     "home_bp/less/home.less",
    #     filters="less,cssmin",
    #     output="dist/css/home.css",
    #     extra={"rel": "stylesheet/less"},
    # )
    # profile_style_bundle = Bundle(
    #     "profile_bp/less/profile.less",
    #     filters="less,cssmin",
    #     output="dist/css/profile.css",
    #     extra={"rel": "stylesheet/less"},
    # )
    # product_style_bundle = Bundle(
    #     "products_bp/less/products.less",
    #     filters="less,cssmin",
    #     output="dist/css/products.css",
    #     extra={"rel": "stylesheet/less"},
    # )
    # JavaScript Bundle
    index_js_bundle = Bundle(
        "index_bp/js/*.js", filters="jsmin", output="dist/js/index.min.js")
    auth_js_bundle = Bundle(
        "auth_bp/js/*.js", filters="jsmin", output="dist/js/auth.min.js")
    dashboard_menu_js_bundle = Bundle(
        "dashboard_bp/js/dashboard_menu.js", filters="jsmin", output="dist/js/dashboard_menu.min.js")
    dashboard_weight_js_bundle = Bundle(
        "dashboard_bp/js/dashboard_weight.js", filters="jsmin", output="dist/js/dashboard_weight.min.js")

    assets.register("index_style_bundle", index_style_bundle)
    assets.register("auth_style_bundle", auth_style_bundle)
    # assets.register("signup_style_bundle", signup_style_bundle)
    assets.register("dashboard_style_bundle", dashboard_style_bundle)

    # assets.register("common_style_bundle", common_style_bundle)
    # assets.register("home_style_bundle", home_style_bundle)
    # assets.register("profile_style_bundle", profile_style_bundle)
    # assets.register("product_style_bundle", product_style_bundle)
    assets.register("index_js_bundle", index_js_bundle)
    assets.register("auth_js_bundle", auth_js_bundle)
    assets.register("dashboard_menu_js_bundle", dashboard_menu_js_bundle)
    assets.register("dashboard_weight_js_bundle", dashboard_weight_js_bundle)

    if app.config["FLASK_ENV"] == "development":
        index_style_bundle.build()
        auth_style_bundle.build()
        # signup_style_bundle.build()
        dashboard_style_bundle.build()
        # common_style_bundle.build()
        # home_style_bundle.build()
        # profile_style_bundle.build()
        # product_style_bundle.build()
        index_js_bundle.build()
        auth_js_bundle.build()
        dashboard_menu_js_bundle.build()
        dashboard_weight_js_bundle.build()
    return assets
