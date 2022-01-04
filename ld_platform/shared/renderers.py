from rest_framework.renderers import JSONRenderer


class JSONResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = {
            "status": "success",
            "code": status_code,
            "data": data,
            "message": None,
        }

        if not str(status_code).startswith("2"):
            response["status"] = "error"
            response["data"] = None
            try:
                response["message"] = data["detail"]
            except (KeyError, TypeError):
                response["data"] = data
        return super(JSONResponseRenderer, self).render(
            response, accepted_media_type, renderer_context
        )
