# https://github.com/TwilioDevEd/automated-survey-django/blob/master/automated_survey/middleware.py


class SMSMiddleware(object):
    def process_request(self, request):
        args = request.POST or request.GET
        request.is_sms = args and args.get("MessageSid")
