import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/languages/wang1287'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
