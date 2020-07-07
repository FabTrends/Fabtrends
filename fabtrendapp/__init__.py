class Cart(object):
    def __init__(self, request):
# ...
# store current applied coupon
        self.coupon_id = self.session.get('coupon_id')