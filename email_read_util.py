import email
import spacy
import textacy
from textacy import preprocessing
from textacy.spacier.doc_extensions import to_tokenized_text

nlp = spacy.load("en_core_web_sm")

# Combine the different parts of the email into a flat list of strings
def flatten_to_string(parts):
    ret = []
    if type(parts) == str:
        ret.append(parts)
    elif type(parts) == list:
        for part in parts:
            ret += flatten_to_string(part)
    elif parts.get_content_type == 'text/plain':
        ret += parts.get_payload()
    return ret

# Extract subject and body text from a single email file
def extract_email_text(path):
    # Load a single email from an input file
    with open(path, errors='ignore') as f:
        msg = email.message_from_file(f)
    if not msg:
        return ""

    # Read the email subject
    subject = msg['Subject']
    if not subject:
        subject = ""

    # Read the email body
    body = ' '.join(m for m in flatten_to_string(msg.get_payload()) if type(m) == str)
    if not body:
        body = ""

    return subject + ' ' + body

# Process a single email file into stemmed tokens
def load(path):
    email_text = extract_email_text(path)
    if not email_text:
        return []

    # use textacy to do the processing, remove the whitesapace, punctuation
    email_text = preprocessing.normalize_whitespace(preprocessing.remove_punctuation(email_text))
    # remove accents and noralize unicode
    email_text = preprocessing.normalize_unicode(preprocessing.remove_accents(email_text))

    # Tokenize the message
    tokens = to_tokenized_text(email_text)

    # Remove stopwords and stem tokens
    if len(tokens) > 2:
        # extract stemming word
        return [w.lemma_ for w in tokens if w not in nlp.Defaults.stopwords]
    return []