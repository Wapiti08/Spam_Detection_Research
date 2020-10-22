'''
   The module to detect the spam through the context of email: subject and text body

'''
from sklearn.model_selection import train_test_split 
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import email_read_util


def read_email_files():
    X = []
    y = [] 
    for i in range(len(labels)):
        filename = 'inmail.' + str(i+1)
        email_str = email_read_util.extract_email_text(Path(DATA_DIR).joinpath(filename))
        X.append(email_str)
        y.append(labels[filename])
    return X, y


X_train, X_test, y_train, y_test, idx_train, idx_test = \
    train_test_split(X, y, range(len(y)), 
    train_size=TRAINING_SET_RATIO, random_state=2)


vectorizer = CountVectorizer()
tfidf_vectorizer = TfidfVectorizer()

X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

# Initialize the classifier and make label predictions
mnb = MultinomialNB()
mnb.fit(X_train_vector, y_train)
y_pred = mnb.predict(X_test_vector)

# Print results
print(classification_report(y_test, y_pred, target_names=['Spam', 'Ham']))
print('Classification accuracy {:.1%}'.format(accuracy_score(y_test, y_pred)))