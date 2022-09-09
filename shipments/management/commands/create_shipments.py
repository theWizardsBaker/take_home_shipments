import math
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from shipments.models import Shipment, ShipmentProduct
from orders.models import Order

class Command(BaseCommand):
    """
        Workflow to create shipments

        find all unfulfiled orders
            -> for each unfulfilled order, find all shipments (if any)
            -> determine what products are left to ship in the current order
            -> ship those products
            -> if no products are left to ship, mark as fulfilled
    """

    help = 'Creates shipments from orders'

    missing_args_message = 'shipments_spacing argument is required'

    DELIVERY_START_DAY = "April 1"
    DELIVERY_END_DAY = "October 1"

    DATE_FORMAT = '%B %d %Y'

    SHIPMENT_DAY_LIMIT = 3

    SHIPMENT_WEIGHT_LIMIT = 5

    def add_arguments(self, parser):
        """
            shipment_spacing: int =
                number of days to space out unfulfilled shipments
        """
        parser.add_argument('shipment_spacing', type=int)
        # should validate these but I'm running out of time
        parser.add_argument('--start_date', type=str)
        parser.add_argument('--end_date', type=str)

    def delivery_dates(self, start_date_str=None, end_date_str=None):
        """

            return the range in which we can deliver

            start_date = start of deliveries
            end_date = end of deliveries

        """
        # calculate default dates
        date = datetime.now()
        if not start_date_str:
            start_date_str = f"{self.DELIVERY_START_DAY} {date.year}"
        if not end_date_str:
            end_date_str = f"{self.DELIVERY_END_DAY} {date.year}"

        return (
            datetime.strptime(start_date_str, self.DATE_FORMAT),
            datetime.strptime(end_date_str, self.DATE_FORMAT)
        )

    def caculate_shipping_dates(self, spacing, start_date, end_date):
        """
            calculate the days we can ship on. We can only ship every (spacing) days:

            business requirement: deliver these products on **three, evenly spaced** shipment dates.

            spacing: int = spacing between shipping days

        """
        # calculate time between dates
        date_delta = end_date - start_date
        # skip by spacing
        return [(start_date + timedelta(days=i)) for i in range(0, date_delta.days + 1, spacing)]

    def unfulfilled_orders(self, date=None):
        """
            calculate all the unfilled orders from our previous year's
            undelivered shipments until date (or today)

            date: date = date to stop looking for unfulfilled orders
        """

        # get all deliveries from the previous year up to now
        previous_year_delivery_end_date = datetime.strptime(f"{self.DELIVERY_END_DAY} {(date).year - 1}", '%B %d %Y')
        # find all unfulfiled orders
        return Order.objects.filter(
            is_fulfilled=False,
            ordered_at__gte=make_aware(previous_year_delivery_end_date),
            ordered_at__lte=make_aware(date),
        ).order_by("ordered_at")

    def handle(self, *args, **options):

        delivery_start_date, delivery_end_date = self.delivery_dates(
            options['start_date'],
            options['end_date']
        )

        # list all the dates we can ship
        all_shipping_dates = self.caculate_shipping_dates(
            options['shipment_spacing'], delivery_start_date, delivery_end_date
        )

        # find the next shipping date based on the current day
        next_shipping_dates = list(filter(lambda ship_date: ship_date > datetime.now(), all_shipping_dates))

        # make sure we have enough days left to ship
        if len(next_shipping_dates) < self.SHIPMENT_DAY_LIMIT: 
            self.stdout.write(f"Not enough time to ship items, only {len(next_shipping_dates)} shipping days remain")
            return

        # fake date for demonstration
        unfulfilled_orders = self.unfulfilled_orders(
            datetime.strptime("June 1 2022", '%B %d %Y')
        )

        self.stdout.write(f"Found {unfulfilled_orders.count()} Order(s) to process:")

        for order in unfulfilled_orders:
            # log each order
            self.stdout.write(f"Order: {order}")

            # get all shipments for order
            shipments = order.shipment_set.all()

            # for each unfulfilled order, find all shipments (if any)
            if shipments.count() > 0:
                """
                    determine what products are left to ship in the current order

                    I don't have time to implement, but i imagine this would pick 
                    up anything that could not ship, maybe due to stock shortage
                    or shipment issues

                    This logic is probably not right
                """
                orders_to_fufill = [] 
                # compare the shipped quantity to the ordered quantity
                for s in shipments:
                    shipment_products = ShipmentProduct.objects.filter(shipment=s)
                    for sp in shipment_products:
                        quantity_difference = sp.product.quantity - sp.quantity
                        if quantity_difference > 0:
                            print(f"Need to ship {quantity_difference} more of {sp.product}")
            else:

                # get all products with the heaviest weights first
                products = order.products.order_by('-item__weight')

                day_to_ship = 0

                # iterate over SHIPMENT_DAY_LIMIT
                while True:

                    new_shipment = Shipment(
                        order=order,
                        has_shipped=False,
                        shipping_weight=0,
                        shipping_date=make_aware(next_shipping_dates[day_to_ship])
                    )

                    new_shipment_products = []

                    for product in products:
                        """
                            business requirement: 
                            shipments must spread out by SHIPMENT_DAY_LIMIT days
                            To whatever extent possible, duplicate `Products` should be sent on different shipment dates.
                        """

                        # move on to the next product if we can't fit this product into our package
                        if (product.item.weight + new_shipment.shipping_weight) > self.SHIPMENT_WEIGHT_LIMIT:
                            continue

                        # if there are still products to pack
                        if product.quantity > 0:
                            # pack_multiples?
                            max_quantity = 1

                            # if we need to pack multiples, find out the quantity needed
                            if product.quantity > self.SHIPMENT_DAY_LIMIT:
                                max_quantity = math.ceil(product.quantity / self.SHIPMENT_DAY_LIMIT)
                                # make sure we can actually fit that quantity
                                while ((max_quantity * product.item.weight) + new_shipment.shipping_weight) > self.SHIPMENT_WEIGHT_LIMIT:
                                    max_quantity -= 1

                            # we could also check the stock here and decrement it
                            # product.item.stock
                            if max_quantity > 0:
                                # pack new product in shipment
                                new_shipment_products.append(
                                    ShipmentProduct(
                                        quantity=max_quantity,
                                        product=product,
                                        shipment=new_shipment
                                    )
                                )
                                # reduce quantity needed
                                product.quantity -= max_quantity
                                # increase package weight
                                new_shipment.shipping_weight += product.item.weight * max_quantity

                    # save shipments
                    new_shipment.save()
                    # save shipment products
                    for sp in new_shipment_products:
                        # reduce stock
                        # sp.product.item.stock -= sp.quantity
                        # sp.product.item.save()
                        sp.save()

                    self.stdout.write(f"\tCreated {new_shipment}: with \n\t{new_shipment_products}")

                    # roll over to the next day
                    day_to_ship += 1
                    if day_to_ship >= self.SHIPMENT_DAY_LIMIT:
                        day_to_ship = 0

                    # if we have no products left to ship, order is complete
                    if sum(p.quantity for p in products) == 0:
                        order.is_fulfilled = True
                        order.save()
                        break
