from http import HTTPStatus


class DocStrings:
    COMMON_ENDPOINT_DOCS: dict = {
        HTTPStatus.UNAUTHORIZED.real: {
            "description": "Raises when unauthorized",
            "content": {
                "application/json": {
                    "example": {"Detail": "Exception raised while decoding JWT token. Insufficient permissions"}
                }
            }
        },
        HTTPStatus.FORBIDDEN.real: {
            "description": "Raises when unauthenticated",
            "content": {
                "application/json": {
                    "example": {"Detail": "Not Authenticated "}
                }
            }
        }
    }

    PUBLISHER_GET_ENDPOINT_DOCS: dict = {
                                            HTTPStatus.OK.real: {
                                                "description": "returns a json with list of publishers",
                                                "content": {
                                                    "application/json": {
                                                        "example": {"publishers": ["kafka", "s3", "bigquery"]}
                                                    }
                                                }
                                            }
                                        } | COMMON_ENDPOINT_DOCS

    PUBLISHER_POST_ENDPOINT_DOCS: dict = {
        HTTPStatus.OK.real: {
            "description": "sends the data to the publishers like kafka, s3, gcs, ...",
            "content": {
                "application/json": {
                    "example": {"publishers": {
                        HTTPStatus.OK.real: ["kafka", "s3", "bigquery"],
                        HTTPStatus.INTERNAL_SERVER_ERROR: ["gcs", "athena"]
                    }}
                }
            }
        },
        HTTPStatus.UNPROCESSABLE_ENTITY.real: {
            "description": "Raises when required parameters are missing",
            "content": {
                "application/json": {
                    "example": {"detail": [{
                        "loc": ["query", "publishers"],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }]
                    }
                }
            }
        },
        HTTPStatus.BAD_REQUEST.real: {
            "description": "Raises when required parameter values are incorrect",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Query param is invalid. Provide publisher values : {'string1'}. Allowed publisher "
                                  "values : {'console', 'file'} "
                    }
                }
            }
        }
    } | COMMON_ENDPOINT_DOCS
