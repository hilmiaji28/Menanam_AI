"""
=========================================================

Response Builder

=========================================================
"""


class ResponseBuilder:

    @staticmethod
    def success(

        tool,

        intent,

        answer,

        **kwargs,

    ):

        response = {

            "tool": tool,

            "intent": intent,

            "status": "success",

            "answer": answer,

            "error": None,

        }

        response.update(kwargs)

        return response

    @staticmethod
    def error(

        tool,

        intent,

        answer,

        error,

        status="error",

        **kwargs,

    ):

        response = {

            "tool": tool,

            "intent": intent,

            "status": status,

            "answer": answer,

            "error": error,

        }

        response.update(kwargs)

        return response