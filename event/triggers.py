# import triggers
# import zserial.serial_read_event_trigger as serial_trigger
import networking.network_read_event_trigger as network_trigger


# event trigger list
_triggers: list = [
    # serial_trigger.check_event,
    network_trigger.check_event
]

def handle_triggers():
    for trigger in _triggers:
        trigger()
