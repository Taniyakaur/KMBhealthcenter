import datetime
import pytz
from visita.models import PrenotazioneVisita
class DateTimeRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, item):
        return self.start <= item < self.end
from django.utils import timezone

def get_slots(orari, date, slot_duration, blocked=None):
    slots = []
    for orario in orari:
        # crea gli slot tra orario.inizio e orario.fine
        current = datetime.datetime.combine(date, orario.inizio)
        end = datetime.datetime.combine(date, orario.fine)
        while current + slot_duration <= end:
            slots.append(current)
            current += slot_duration

    # Rimuovi slot bloccati
    if blocked:
        for block in blocked:
            block_range = DateTimeRange(block['start'], block['end'])
            slots = [s for s in slots if s not in block_range]

    # Rimuovi slot già prenotati
    prenotazioni = PrenotazioneVisita.objects.filter(data=date)
    for p in prenotazioni:
        pren_range = DateTimeRange(
            datetime.datetime.combine(date, p.ora),
            datetime.datetime.combine(date, (datetime.datetime.combine(date, p.ora) + datetime.timedelta(minutes=30)).time())
        )
        slots = [s for s in slots if s not in pren_range]

    return slots