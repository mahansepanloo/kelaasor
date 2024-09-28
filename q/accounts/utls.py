from kavenegar import *

def send_otp_code(phone_number, code):
	try:
		api = KavenegarAPI('mqhod')
		params = {
			'sender': '',
			'receptor': phone_number,
			'message': f' اعتبار کد 100 ثانیه{code} کد تایید شما '
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)
