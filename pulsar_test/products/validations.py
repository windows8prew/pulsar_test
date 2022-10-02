import six

from filters.schema import base_query_params_schema
from filters.validations import IntegerLike

product_query_schema = base_query_params_schema.extend({
    "status": IntegerLike(),
    "article": six.text_type,
    "name": six.text_type,
})
