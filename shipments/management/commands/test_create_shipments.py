from io import StringIO

from django.test import TestCase
from django.core import management
from django.core.management.base import CommandError

from .create_shipments import Command


class CreateShipmentsCommandTests(TestCase):

    def test_not_found(self):
        out = StringIO()
        args = [3]
        management.call_command('create_shipments', *args, stdout=out)
        self.assertEquals(out.getvalue(), "Found 0 Order(s) to process:\n")

    def test_delivery_dates(self):
        cmd = Command()
        start_date_str = 'April 01 2020'
        end_date_str = 'June 01 2020'
        delivery_date = cmd.delivery_dates(start_date_str, end_date_str)

        self.assertEquals(
            start_date_str,
            delivery_date[0].strftime('%B %d %Y')
        )

    def test_caculate_shipping_dates(self):
        cmd = Command()
        start_date_str = 'May 01 2020'
        end_date_str = 'June 01 2020'
        delivery_date = cmd.delivery_dates(start_date_str, end_date_str)

        shipping_dates = cmd.caculate_shipping_dates(15, delivery_date[0], delivery_date[1])

        self.assertEquals(
            len(shipping_dates),
            3
        )

        shipping_dates = cmd.caculate_shipping_dates(20, delivery_date[0], delivery_date[1])

        self.assertEquals(
            len(shipping_dates),
            2
        )

        number_of_days = delivery_date[1] - delivery_date[0]

        shipping_dates = cmd.caculate_shipping_dates(1, delivery_date[0], delivery_date[1])

        self.assertEquals(
            len(shipping_dates),
            number_of_days.days
        )
