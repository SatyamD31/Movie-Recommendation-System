from flask import Flask, request, url_for, redirect, render_template
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, template_folder='templates')

############################################################################################################################################
                                                            #Movies#
############################################################################################################################################
dfm = pd.read_csv('Datasets/finMov.csv')

count = CountVectorizer(stop_words='english')
count_matrix_m = count.fit_transform(dfm['soup'])
csm_m = cosine_similarity(count_matrix_m, count_matrix_m)

dfm = dfm.reset_index()
# indices_m = pd.Series(dfm.index, index=dfm['Movie'])
indices_m = pd.Series(dfm.index, index=dfm['index_m'])
# allTitles_m = [dfm['Movie'][i] for i in range(len(dfm['Movie']))]
allTitles_m = [dfm['index_m'][i] for i in range(len(dfm['index_m']))]

def recommend_m(title, csm_m=csm_m):

    # name = []
    # year = []
    # rating = []
    # genre = []

    # csm_m = cosine_similarity(count_matrix_m, count_matrix_m)
    idx_m = indices_m[title]
    sim_scores_m = list(enumerate(csm_m[idx_m]))
    sim_scores_m = sorted(sim_scores_m, key=lambda x: x[1], reverse=True)
    sim_scores_m = sim_scores_m[1:11]
    movieIndices = [i[0] for i in sim_scores_m]

    name = dfm['Movie'].iloc[movieIndices]
    year = dfm['Release Year'].iloc[movieIndices]
    rating = dfm['IMDB Rating'].iloc[movieIndices]
    genre = dfm['Genre'].iloc[movieIndices]

    # df_final = pd.DataFrame[{'Title': name, 'Release Year': year, 'IMDB Rating': rating, 'Genre': genre}]
    df_final = pd.DataFrame(columns=['Title', 'Release Year', 'IMDB Rating', 'Genre'])
    df_final['Title'] = name
    df_final['Release Year'] = year
    df_final['IMDB Rating'] = rating
    df_final['Genre'] = genre
    
    return df_final

############################################################################################################################################
                                                            #TV Series#
############################################################################################################################################

dft = pd.read_csv('Datasets/tvs.csv')

count = CountVectorizer(stop_words='english')
count_matrix_t = count.fit_transform(dft['soup'])
csm_t = cosine_similarity(count_matrix_t, count_matrix_t)

dft = dft.reset_index()
# indices_t = pd.Series(dft.index, index=dft['Series'])
indices_t = pd.Series(dft.index, index=dft['index_t'])
# allTitles_t = [dft['Series'][i] for i in range(len(dft['Series']))]
allTitles_t = [dft['index_t'][i] for i in range(len(dft['index_t']))]

def recommend_t(title, csm_t=csm_t):
    csm_t = cosine_similarity(count_matrix_t, count_matrix_t)
    idx_t = indices_t[title]
    sim_scores_t = list(enumerate(csm_t[idx_t]))
    sim_scores_t = sorted(sim_scores_t, key=lambda x: x[1], reverse=True)
    sim_scores_t = sim_scores_t[1:11]
    tvsIndices = [i[0] for i in sim_scores_t]

    name = dft['Series'].iloc[tvsIndices]
    year = dft['Release Year'].iloc[tvsIndices]
    rating = dft['IMDB Rating'].iloc[tvsIndices]
    genre = dft['Genre'].iloc[tvsIndices]

    df_final = pd.DataFrame(columns=['Title', 'Release Year', 'IMDB Rating', 'Genre'])
    df_final['Title'] = name
    df_final['Release Year'] = year
    df_final['IMDB Rating'] = rating
    df_final['Genre'] = genre
    
    return df_final

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        msName = request.form['movieName']
        # msName = msName.title()

        if msName not in allTitles_m:
            return render_template('unavailable.html', query=msName)
            # return redirect(url_for('unavailable.html', name=msName))
        else:
            result = recommend_m(msName)
            names = []
            years = []
            ratings = []
            genres = []
            for i in range(len(result)):
                names.append(result.iloc[i][0])
                years.append(result.iloc[i][1])
                ratings.append(result.iloc[i][2])
                genres.append(result.iloc[i][3])

            return render_template('available.html', name=names, year=years, rating=ratings, genre=genres, query=msName)
            # return redirect(url_for('available.html', name=names, year=years, rating=ratings, genre=genres, query=msName))
            # return render_template('movies.html', query=msName)
    return render_template('movies.html')

@app.route('/tvSeries', methods=['GET', 'POST'])
def tvSeries():
    if request.method == 'POST':
        msName = request.form['movieName']
        # msName = msName.title()

        if msName not in allTitles_t:
            return render_template('unavailable.html', query=msName)
            # return redirect(url_for('unavailable.html', name=msName))
        else:
            result = recommend_t(msName)
            names = []
            years = []
            ratings = []
            genres = []
            for i in range(len(result)):
                names.append(result.iloc[i][0])
                years.append(result.iloc[i][1])
                ratings.append(result.iloc[i][2])
                genres.append(result.iloc[i][3])

            return render_template('available.html', name=names, year=years, rating=ratings, genre=genres, query=msName)
            # return redirect(url_for('available.html', name=names, year=years, rating=ratings, genre=genres, query=msName))
    return render_template('tvSeries.html')

if __name__ == '__main__':
    app.debug = True
    app.run()