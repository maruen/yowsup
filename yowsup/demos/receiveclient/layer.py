from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
import threading
import logging
import datetime
import time
import subprocess
import shlex

logger = logging.getLogger(__name__)

class EchoLayer(YowInterfaceLayer):

    PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue"
    PROP_CREDENTIALS = "org.openwhatsapp.yowsup.prop.auth.credentials"

    def __init__(self):
        super(EchoLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()


    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over
        #print str(messageProtocolEntity.getFrom()) + ' - ' + str(messageProtocolEntity.getBody())
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())

	line = self.getProp(self.__class__.PROP_CREDENTIALS)[2]
	ts = time.time()
	at = messageProtocolEntity.getFrom().find('@');
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S_+{0}').format(messageProtocolEntity.getFrom()[0:at])
	filename = '/var/spool/atsms/{0}/inbox/{1}'.format(line,timestamp)
	f = open(filename,'w')
	f.write(messageProtocolEntity.getBody())
	f.close()
	print str('Running runOnReceive.sh for {0}'.format(line))
	subprocess.call(shlex.split('/var/spool/atsms/runOnReceive.sh {0}'.format(line)))

        self.toLower(receipt)
	#raise KeyboardInterrupt()

    @ProtocolEntityCallback("send_message")
    def sendMessage(self, destination, message, messageProtocolEntity):
        outgoingMessageProtocolEntity = TextMessageProtocolEntity(message,to = destination + "@s.whatsapp.net")
        self.toLower(outgoingMessageProtocolEntity)


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery", entity.getFrom())
        self.toLower(ack)

    
    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        self.lock.acquire()
        for target in self.getProp(self.__class__.PROP_MESSAGES, []):
            phone, message = target
            if '@' in phone:
                messageEntity = TextMessageProtocolEntity(message, to = phone)
            elif '-' in phone:
                messageEntity = TextMessageProtocolEntity(message, to = "%s@g.us" % phone)
            else:
                messageEntity = TextMessageProtocolEntity(message, to = "%s@s.whatsapp.net" % phone)
            self.ackQueue.append(messageEntity.getId())
            self.toLower(messageEntity)
        self.lock.release()

    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()

        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            logger.info("Message sent")
            #raise KeyboardInterrupt()

        self.lock.release()
