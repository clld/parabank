import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/languages'),
        ('get_html', '/parameters'),
        ('get_html', '/languages/abau1245'),
        ('get_html', '/parameters/2sg_a'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
