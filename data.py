from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.feature_extraction import text 

stop_words = text.ENGLISH_STOP_WORDS.union([
    "carpediem", "Carpediem", "olin", "lists", "students", "listinfo", "edu",
    "3d", "font", "style", "mso", "xmlns", "skipped", "multipart", "alternative",
    "content", "type", "bounces", "sent", "mailto", "subject", "fw",
    "_______________________________________________",
])

client = MongoClient('localhost', 27017)
email_collection = client["carpe"]["emails"]
emails = email_collection.find().limit(30000)
documents = [email.get("subject", False) for email in emails if not False]
# documents = ["aidan"]

vectorizer = TfidfVectorizer(stop_words=stop_words, min_df=10)
X = vectorizer.fit_transform(documents)


def test_k(k_val):
    true_k = k_val
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=1000, n_init=1)
    model.fit(X)
    print("\n")
    print("Top terms per cluster (" + str(k_val) + " clusters!):")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print "Cluster %d:" % i,
        print " ".join([terms[ind] for ind in order_centroids[i, :5]])

if __name__ == "__main__":
    [test_k(i) for i in range(5, 15)]
