from liqpay import LiqPay
import os

def get_liqpay_instance():
    return LiqPay(
        os.getenv("LIQPAY_PUBLIC_KEY"),
        os.getenv("LIQPAY_PRIVATE_KEY")
    )
