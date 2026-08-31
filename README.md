Real-Time Google Play Store Analysis - 
      An interactive Google Play Store Data Analysis and Visualization Dashboard built with Python, Pandas, Plotly, NLTK, and Django. The project analyzes Google Play Store application metadata and user reviews to uncover         patterns in app categories, installs, ratings, pricing, revenue, genres, updates, and review sentiment. The analysis is presented through an interactive web dashboard with Plotly visualizations.


Project Objective - 
      The main objective of this project is to transform Google Play Store application and review data into meaningful visual insights that can help understand:
          i) Which app categories are most common
         ii) How free and paid apps are distributed
        iii) How ratings are distributed
         iv) Which categories receive the most installs
          v) How frequently applications are updated
         vi) Which categories generate the most estimated revenue
        vii) Which genres are most common
        vii) Whether app updates are associated with ratings
       viii) Differences between free and paid app ratings
         ix) Overall sentiment in user reviews
          x) Relationships between app size, ratings, and installs
         xi) Growth of installs over time
        xii) Differences between average ratings, reviews, installs, and revenue


Technologies Used - 

Technology                                                       Purpose

Python                                                           Core programming and data analysis

Pandas                                                           Data cleaning, transformation, grouping and aggregation

NumPy                                                            Numerical calculations and feature engineering

Plotly Express                                                   Interactive charts and dashboard visualizations

Plotly Graph Objects                                             Advanced/custom interactive visualizations

NLTK VADER                                                       Sentiment analysis of user reviews

Django                                                           Web application and dashboard backend

Pytz                                                             IST-based time-window logic

HTML/CSS                                                         Dashboard presentation layer


Dashboard Visualizations - 
    The dashboard contains 16 analytical visualizations.

  1. Top Categories on Play Store - 
     Chart Type: Bar Chart
     Shows the 10 categories with the highest number of applications.
     Insight: The dashboard indicates that categories such as Tools, Entertainment, and Productivity have a strong presence in the dataset.

  2. App Type Distribution - 
     Chart Type: Pie Chart
     Compares Free and Paid applications.
     Insight: Most applications are free, suggesting that free distribution is the dominant model in the dataset, with monetization potentially coming through advertising or in-app purchases.

  3. Rating Distribution - 
     Chart Type: Histogram
     Shows how application ratings are distributed.
     Insight: Ratings are concentrated toward the higher end of the scale, indicating that a large proportion of applications receive relatively favorable ratings.

  4. Installs by Category - 
     Chart Type: Bar Chart
     Ranks categories according to total application installs.
     Insight: Social and Communication categories have particularly high install volumes, reflecting their broad usage and frequent engagement.

  5. Number of Updates over the Year - 
     Chart Type: Line Chart
     Shows the number of application records associated with each update year.
     Insight: The trend suggests increasing update activity over the analyzed period, indicating active maintenance and improvement of applications.

  6. Revenue by Category - 
     Chart Type: Bar Chart
     Compares estimated revenue across categories.
     Insight: Business and Productivity categories are highlighted as strong revenue-generating segments, demonstrating their monetization potential in the dataset.

  7. Top Genres - 
     Chart Type: Bar Chart
     Displays the most common genres after splitting multi-genre records.
     Insight: Action and Casual are among the most common genres, showing strong representation of gaming-oriented applications.

  8. Impact of Rating on Last Update - 
     Chart Type: Scatter Plot
     Examines the relationship between: i) Last Updated date, ii) Application rating, iii) Application type
     Insight: The visualization suggests a weak relationship between update timing and ratings. Updating an application more frequently does not necessarily result in a higher rating.

  9. Rating for Paid vs Free Apps - 
     Chart Type: Box Plot
     Compares rating distributions between free and paid applications.
     Insight: The analysis indicates that paid applications generally have higher ratings than free applications, suggesting that users may have higher expectations for applications they pay for.

 10. Sentiment Distribution - 
     Chart Type: Bar Chart
     Uses NLTK VADER sentiment analysis on translated user reviews.
     Insight: User reviews contain both positive and negative feedback, with the overall distribution showing a slight tendency toward positive sentiment.
     
Time-Windowed Advanced Visualizations
     Visualizations 11–16 use the current Asia/Kolkata (IST) time and are deliberately enabled only during specified time windows. This makes the dashboard behave as a time-aware analytical application rather than simply       displaying static charts.

 11. App Size vs Average Rating - 
     Chart Type: Bubble/Scatter Plot
     Available: 5 PM – 7 PM IST
     Examines: i) App size, ii) Average rating, iii) Installs, iv) Category
     Insight: The visualization emphasizes highly installed applications and examines how application size relates to average rating.

 12. Global App Installs by Category - 
     Chart Type: Animated Choropleth Map
     Available: 6 PM – 8 PM IST
     The analysis attempts to infer country information from application names and visualizes high-install categories geographically.
     (NOTE: In my dataset there is no 'Country' column present, thus I have generated the column with my own, so it is a bit different because it only shows installs as most of the countries are unknown.)
     Insight: The chart focuses on categories exceeding the one-million-install threshold. Because country information is inferred from app-name keywords rather than an explicit country field, the geographic interpretation should be treated cautiously.
     
 14. Total Installs over Time
     Chart Type: Line Chart
     Available: 6 PM – 9 PM IST
     Tracks categories where install growth exceeds 20%.
     Insight: The dashboard highlights particularly strong growth around August 2017 to September 2018, while other periods remain comparatively stable.

 15. Cumulative Installs over Time - 
     Chart Type: Area Chart
     Available: 4 PM – 6 PM IST
     Analyzes cumulative installs for selected categories based on filtering conditions such as: i) Rating ≥ 4.2, ii) More than 1,000 reviews, iii) App size between 20 MB and 80 MB
     Insight: The visualization focuses on highly rated applications with substantial review counts and tracks their cumulative installation growth over time.

 16. Average Rating vs Total Review Count - 
     Chart Type: Grouped Bar Chart
     Available: 3 PM – 5 PM IST
     Compares normalized: i) Average rating, ii) Total review count
     Insight: The comparison is restricted to applications with ratings of at least 4.0 and focuses on applications updated during January.

 17. Average Installs vs Average Revenue — Free vs Paid - 
     Chart Type: Dual-Axis Grouped Bar Chart
     Available: 1 PM – 2 PM IST
     Compares: i) Average installs, ii) Average revenue, iii) Application type, iv) Category
     Insight: The filtered dataset emphasizes applications meeting install, revenue, Android-version, size, content-rating, and name-length conditions. The analysis highlights the behavior of paid applications within the selected subset.


Key Findings - 
    1) The dashboard provides several important high-level observations:
    2) Tools, Entertainment and Productivity are among the strongest categories by application count.
    3) Free applications dominate the dataset.
    4) Application ratings are generally concentrated toward the higher rating range.
    5) Social and Communication categories have very high install volumes.
    6) Application update activity increases across the analysed years.
    7) Business and Productivity show strong estimated monetization potential.
    8) Action and Casual are prominent genres.
    9) Last-update frequency shows only a weak relationship with ratings.
   10) Paid applications generally show higher ratings than free applications.
   11) User review sentiment is mixed but shows a slight positive tendency.
   12) Advanced analyses explore relationships between app size, ratings, installs, reviews, and revenue.
   13) The dashboard includes time-aware visualizations that become available during specified IST windows.


Project Summary - 
    This project combines data analytics, natural language processing, interactive visualization, and web development into a single Google Play Store analytics platform.
    It demonstrates an end-to-end workflow:
        Raw Data → Cleaning → Feature Engineering → Sentiment Analysis → Visualization → Django Dashboard → Deployment
