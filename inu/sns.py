import boto3
from .password import get_aws_access_key_id, get_aws_secret_access_key, get_number, get_region


class SNSConnection:
    def __init__(self):
        # Create an SNS client
        self.client = boto3.client(
            "sns",
            aws_access_key_id=get_aws_access_key_id(),
            aws_secret_access_key=get_aws_secret_access_key(),
            region_name=get_region()
        )

        self.client.set_sms_attributes(
            attributes={
                'DefaultSenderID': 'InuSecure',
                'DefaultSMSType': 'Transactional'
            }
        )

    def insert(self, otp, number=get_number()):
        message = "Your OTP is " + otp + "."
        # Send your sms message.
        self.client.publish(
            PhoneNumber=number,
            Message=message
        )