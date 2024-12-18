from flask import Flask,render_template,request
import pickle
import numpy as np
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app=Flask(__name__)

@app.route('/')

def index():
    # returning all the columns of popular_df such that it can be shown correctly to the webpage(for top 50 books)
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           # i want to have all ratings rounded of two decimal places 
                           rating=list(map(lambda x: round(x,2),popular_df['avg_rating'].values))
                           )
    
    
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')  # Getting the input from the user (book name)
    try:
        # Find the index of the user_input in the pivot table (pt)
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]  # Top 4 similar books

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        return render_template('recommend.html', data=data)

    except IndexError:
        # Handle case when no recommendations are found
        return render_template('recommend.html', data=None, error_message="No recommendations found for the entered book.")


if __name__=='__main__':
    app.run(debug=True)
