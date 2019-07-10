import argparse


def parse_cli():
    parser = argparse.ArgumentParser(description='Account Monitor')
    parser.add_argument('--broker', type=str, required=True, help='BrokerID')
    parser.add_argument('--investor', type=str, required=True, help='InvestorID')
    parser.add_argument('--password', type=str, required=True, help='Password')
    parser.add_argument('--app_id', type=str, required=True, help='APP ID')
    parser.add_argument('--auth_code', type=str, required=True, help='Authentication Code')
    parser.add_argument('--front_addr', type=str, required=True, help='Front Address')
    return parser.parse_args()
