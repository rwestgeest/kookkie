#!/usr/bin/env python3
import asyncio
from aiosmtpd.controller import Controller
import ssl
from aiosmtpd.smtp import SMTP

class TLSController(Controller):
    def __init__(self, handler, hostname, port, tls_context):
        super().__init__(handler=handler, hostname=hostname, port=port)
        self.tls_context = tls_context
        
    def factory(self):
        return SMTP(self.handler, enable_SMTPUTF8=True, tls_context=self.tls_context)

class SmtpHandler:
    def __init__(self):
        self.messages = []

    async def handle_DATA(self, server, session, envelope):
        data = envelope.content.decode('utf8', errors='replace')
        print(data)
        if 'generate-data-error' in data: return '554 Transaction failed: Local address contains control or whitespace'
        return '250 Message accepted for delivery'


async def main(loop):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('cert.pem', 'key.pem')

    controller = TLSController(SmtpHandler(), hostname='0.0.0.0', port=2525, tls_context=context)
    controller.start()

if __name__ == '__main__':
    print("starting smtp server")
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop=loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
