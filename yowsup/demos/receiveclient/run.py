from layer import EchoLayer
from yowsup.layers.auth import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.protocol_presence import YowPresenceProtocolLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.coder import YowCoderLayer
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup import env
import sys

#CREDENTIALS = ("5511964958455", "R7U1GjrXKN7j/Jw9SdlF5xcJJWY=") # replace with your phone and password
def send_message(destination, message):

    ''' destination is <phone number> without '+'
        and with country code of type string,
        message is string
        e.g send_message('11133434343','hello')
    '''
    messages = [(destination, message)]
    layers = (EchoLayer,
              (YowAuthenticationProtocolLayer,
               YowMessagesProtocolLayer,
               YowReceiptProtocolLayer,
               YowAckProtocolLayer,
               YowPresenceProtocolLayer)
              ) + YOWSUP_CORE_LAYERS
    stack = YowStack(layers)
    stack.setProp(EchoLayer.PROP_MESSAGES, messages)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
    # Setting credentials
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)

    # WhatsApp server address
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)              
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())

    # Sending connecting signal
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    try:
        # Program main loop
        stack.loop()
    except AuthError as e:
        print('Authentication error %s' % e.message)
        sys.exit(1)

def receive_message(credentials):

    layers = (  EchoLayer,
                (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer,
                YowReceiptProtocolLayer, YowAckProtocolLayer,
                YowPresenceProtocolLayer)
             ) + YOWSUP_CORE_LAYERS

    stack = YowStack(layers)
    # Setting credentials
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials)

    # WhatsApp server address
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())

    stack.setProp(EchoLayer.PROP_CREDENTIALS, credentials)

    # Sending connecting signal
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    try:
        # Program main loop
        stack.loop()
    except AuthError as e:
        print('Authentication error %s' % e.message)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('%s send number message\nrecv\n' % sys.argv[0])
        sys.exit(1)
    if sys.argv[1] == 'send':
        try:
            send_message(sys.argv[2],sys.argv[3])
        except KeyboardInterrupt:
            print('closing')
            sys.exit(0)
    if sys.argv[1] == 'recv':
        try:
            receive_message()
        except KeyboardInterrupt:
            print('closing')
            sys.exit(0)
