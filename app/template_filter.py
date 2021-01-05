def register_template_filter(app):
    @app.template_filter("sex_replace")
    def sex_replace(value):
        sex_map = {
            0: "女生",
            1: "男生",
            2: "保密"
        }
        return sex_map.get(value, "未知")