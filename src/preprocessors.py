from sklearn import ensemble, lda, preprocessing, decomposition, cluster

best = (
    'best',
    ensemble.ExtraTreesClassifier(n_estimators=250, random_state=0))
scale = ('scale', preprocessing.StandardScaler())
normalize = ('normalize', preprocessing.Normalizer())
unit = ('unit', preprocessing.MinMaxScaler())
pca = ('pca', decomposition.PCA(n_components="mle"))
lda = ('lda', lda.LDA(solver='eigen', shrinkage='auto'))
whiten = ('whiten', decomposition.PCA(n_components="mle", whiten=True))
kmeans = ('kmeans', cluster.KMeans(n_clusters=50))

preprocessors = dict([best, scale, normalize, unit, pca, lda, whiten, kmeans])

no_params = [{}]
