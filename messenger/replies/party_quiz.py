import json
import random

from django.utils.translation import ugettext as _

from messenger import intents
from messenger.api import get_user_profile
from messenger.api.formatters import format_text, format_image_attachment, format_quick_replies
from messenger.formatters.party_quiz import format_party_quiz_alternatives
from messenger.replies.generic_quiz import get_quiz_completed_replies
from messenger.utils import save_answers, get_next_manuscript

from quiz.models import Manuscript, QuizAlternative, QuizAnswer
from quiz.utils import PARTY_SHORT_NAMES


def get_quiz_level_replies(sender_id, session, payload, text):
    """ Show available skill levels as quick replies """
    buttons = []
    for val, level in Manuscript.LEVEL_CHOICES:
        buttons.append({
            "content_type": "text",
            "title": str(level),
            "payload": json.dumps({
                'level': val,
                'intent': intents.INTENT_NEXT_ITEM
            }),
        })

    return [format_quick_replies(sender_id, buttons, text)]


def get_quiz_party_question_replies(sender_id, session, payload):
    """ Show question for given hdo category"""
    return [format_party_quiz_alternatives(sender_id, session.meta['manuscript'])]


def _get_next_text(alt: QuizAlternative):
    positive_emojis = ['👍', '😃', '👌', '❤', '👏', '💪', '👊']
    negative_emojis = ['💩']
    if alt.correct_answer:
        return 'Riktig! {}'.format(random.choice(positive_emojis))

    correct_alt = alt.get_correct_in_same_manuscript()
    correct_text = ''
    if correct_alt:
        correct_text = ' Riktig svar er {}'.format(PARTY_SHORT_NAMES[correct_alt.text])

    return 'Feil {}{}'.format(random.choice(negative_emojis), correct_text)


def get_party_quiz_answer_replies(sender_id, session, payload, answer: QuizAnswer):
    try:
        alt = QuizAlternative.objects.get(pk=payload['alternative'])
    except QuizAlternative.DoesNotExist:
        return []

    next_text = _get_next_text(alt)

    next_manuscript = get_next_manuscript(session, quiz=True)
    if next_manuscript:
        session.meta['next_manuscript'] = next_manuscript.pk if next_manuscript else None
        return [format_text(sender_id, next_text)]

    return get_quiz_completed_replies(sender_id, session)


def get_quiz_broken_question_replies(sender_id, session, payload=None):
    """ Get replies to quiz answers INTENT_ANSWER_QUIZ_QUESTION """
    first_name = session.meta['first_name']
    if not first_name:
        first_name = session.meta['first_name'] = get_user_profile(sender_id)['first_name']

    # Get last asked promise
    p_i = session.meta['promise']
    if p_i > 0:
        p_i -= 1
    promise = session.meta['manuscript']['promises'][p_i]

    # Is answer correct?
    if payload['answer'] == promise['status']:
        text = 'Godt svar {} 🙂 Det løftet ble {}'.format(first_name, _(promise['status']))
    else:
        text = 'Beklager {} 😩  Det var ikke riktig, det løftet ble {}'.format(first_name, _(promise['status']))

    replies = [format_text(sender_id, text)]

    # Try to get a random image of correct type and display 1 out of 3 times
    images = list(filter(lambda x: x['type'] == promise['status'], session.meta['manuscript']['images']))
    if images and session.meta['promise'] % 3 == 0:
        image = random.choice(images)
        replies += [format_image_attachment(sender_id, image['url'])]

    # Is last promise?
    if session.meta['promise'] == len(session.meta['manuscript']['promises']):
        save_answers(session)

    # Update answer state
    current_answers = session.meta.get('answers', {})
    current_answers[payload['question']] = payload['answer']
    session.meta['answers'] = current_answers

    return replies
