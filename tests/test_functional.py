import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/languages/wang1287'),
        ('get_html', '/languages/casi1235#pronouns'),
        ('get_html', '/parameters/mF'),
        ('get_html', '/patterns/22'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
