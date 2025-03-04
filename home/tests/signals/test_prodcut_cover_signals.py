import os
from unittest import mock

from django.conf import settings
from django.test import TestCase

from home.models import Products


class TestProductCoverDelete(TestCase):
    @mock.patch('os.remove')
    def test_delete_cover_when_product_is_deleted(self, mock_remove):
        product = Products.objects.create(
            name="Test Product",
            cover="path/to/cover.jpg",
            price=100.00,
            description="Test Description",
            slug="test-product"
        )

        product.delete()

        mock_remove.assert_called_with(product.cover.path)

    @mock.patch('os.remove')
    def test_delete_old_cover_when_product_cover_is_updated(self, mock_remove):
        product = Products.objects.create(
            name="Test Product",
            cover="path/to/old_cover.jpg",
            price=100.00,
            description="Test Description",
            slug="test-product"
        )

        product.cover = "path/to/new_cover.jpg"
        product.save()

        old_cover_path = os.path.join(
            settings.MEDIA_ROOT,
            "path", "to", "old_cover.jpg"
        )
        mock_remove.assert_called_with(old_cover_path)
