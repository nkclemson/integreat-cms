import pytest

from ..utils import check_view_status_code
from ..view_config import PARAMETRIZED_VIEWS


@pytest.mark.django_db
@pytest.mark.parametrize("view_name,kwargs,post_data,roles", PARAMETRIZED_VIEWS[6::16])
def test_view_status_code_6(
    login_role_user, caplog, view_name, kwargs, post_data, roles
):
    check_view_status_code(login_role_user, caplog, view_name, kwargs, post_data, roles)
