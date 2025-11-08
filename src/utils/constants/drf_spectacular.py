from drf_spectacular.utils import OpenApiResponse, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# ---------------------------------------------------------------------
# parameters
# ---------------------------------------------------------------------

AUTH_API_HEADER = OpenApiParameter(
    name="Authorization",
    type=str,
    location=OpenApiParameter.HEADER,
    required=True,
    description="Bearer token",
)

# ---------------------------------------------------------------------
# responses
# ---------------------------------------------------------------------

ACCESS_TOKEN_API_RESPONSE = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            "Access Token Response",
            value={"access_token": "token"},
        )
    ],
)

MESSAGE_SUCCESS_API_RESPONSE = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    examples=[OpenApiExample("successful response", value={"message": "string"})],
)
