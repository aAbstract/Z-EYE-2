# event type to function map
subscribers = {}


def subscribe(event_type: str, func):
    ''' add function @func to event @event_type '''

    # create event type if not exist
    if not event_type in subscribers:
        subscribers[event_type] = []

    # pind function to event type
    subscribers[event_type].append(func)


def post_event(event_type: str, data):
    ''' trigger certain event @event_type with arguments @data '''

    # if there is no functions listed under that event then do nothing
    if not event_type in subscribers:
        return

    # execute all functions listeninig in certain event
    for func in subscribers[event_type]:
        func(data)
