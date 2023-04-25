class HighestRatedRecommender(Recommender):
    """
    Base recommender class.
    """

    def __init__(self):
        """
        Initialize base recommender params and variables.
        """
        # Write your code here
        self.highest_rated_films = None

    def fit(self, interactions_df, users_df, items_df):
        """
        Training of the recommender.

        :param pd.DataFrame interactions_df: DataFrame with recorded interactions between users and items
            defined by user_id, item_id and features of the interaction.
        :param pd.DataFrame users_df: DataFrame with users and their features defined by user_id and the user feature columns.
        :param pd.DataFrame items_df: DataFrame with items and their features defined by item_id and the item feature columns.
        """
        # Write your code here
        interactions_df = ml_ratings_df.copy()
        items_df = ml_movies_df.copy()
        # display(interactions_df)
        # display(items_df)

        ratings_count = interactions_df.groupby('item_id')['rating'].count()
        selected_films = interactions_df[['item_id', 'rating']]
        selected_films = selected_films.loc[selected_films['item_id'].isin(ratings_count[ratings_count >= 50].index)]
        self.highest_rated_films = selected_films.groupby('item_id').mean().sort_values(by='rating',
                                                                                        ascending=False).reset_index()

    def recommend(self, users_df, items_df, n_recommendations=1):
        """
        Serving of recommendations. Scores items in items_df for each user in users_df and returns
        top n_recommendations for each user.

        :param pd.DataFrame users_df: DataFrame with users and their features for which recommendations should be generated.
        :param pd.DataFrame items_df: DataFrame with items and their features which should be scored.
        :param int n_recommendations: Number of recommendations to be returned for each user.
        :return: DataFrame with user_id, item_id and score as columns returning n_recommendations top recommendations
            for each user.
        :rtype: pd.DataFrame
        """

        # Write your code here

        recommendations = pd.DataFrame(columns=['user_id', 'item_id', 'score'])

        for ix, user in users_df.iterrows():
            user_recommendations = pd.DataFrame({'user_id': user['user_id'],
                                                 'item_id': self.highest_rated_films['item_id'][:n_recommendations],
                                                 'score': self.highest_rated_films['rating'][:n_recommendations]})

            recommendations = pd.concat([recommendations, user_recommendations])

        recommendations = recommendations.reset_index(drop=True)
        return recommendations