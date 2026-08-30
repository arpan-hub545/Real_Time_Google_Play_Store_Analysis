import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import nltk
nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import webbrowser
from datetime import datetime
import pytz
import joblib

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
apps_data = pd.read_csv(BASE_DIR / "Play Store Data.csv")
reviews_data = pd.read_csv(BASE_DIR / "User Reviews.csv")

apps_data = apps_data.dropna(subset=['Rating'])
for column in apps_data.columns:
    apps_data[column].fillna(apps_data[column].mode()[0],inplace=True)
apps_data.drop_duplicates(inplace=True)
apps_data = apps_data[apps_data['Rating']<=5]
reviews_data = reviews_data.dropna(subset=['Translated_Review'])

apps_data['Reviews'] = apps_data['Reviews'].astype(int)
apps_data['Installs'] = apps_data['Installs'].astype(str).str.replace(',','').str.replace('+','').astype(int)
apps_data['Price'] = apps_data['Price'].astype(str).str.replace('$','').astype(float)

apps_data['Log_Installs'] = np.log(apps_data['Installs'])
apps_data['Log_Reviews'] = np.log(apps_data['Reviews'])
apps_data['Revenue'] = apps_data['Price']*apps_data['Installs']

def convert_size(size):
    if 'M' in size:
        return float(size.replace('M',''))
    elif 'k' in size:
        return float(size.replace('k',''))/1024
    else:
        return np.nan

apps_data['Size'] = apps_data['Size'].apply(convert_size)

def rating_group(rating):
    if rating >= 4:
        return 'Top Rated App'
    elif rating >= 3:
        return 'Above Average'
    elif rating >= 2:
        return 'Average'
    else:
        return 'Below Average'

apps_data['Rating_Group'] = apps_data['Rating'].apply(rating_group)

sia = SentimentIntensityAnalyzer()

reviews_data['Sentiment_Score'] = reviews_data['Translated_Review'].apply(lambda x: sia.polarity_scores(str(x))['compound'])

apps_data['Last Updated'] = pd.to_datetime(apps_data['Last Updated'], errors='coerce')
apps_data['Year'] = apps_data['Last Updated'].dt.year

merged_data = pd.merge(apps_data,reviews_data,on='App',how='inner')

plot_width = 400
plot_height = 300
plot_bg_color = 'black'
text_color = 'white'
title_font = {'size':16}
axis_font = {'size':12}


plot_containers_11 = []
def save_plot_as_html(fig, filename, insight):

    html_content = pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs=False
    )


    plot_containers_11.append({

        "filename": filename,

        "plot_html": html_content,

        "insight": insight

    })
    
#figure 1
category_count = apps_data['Category'].value_counts().nlargest(10)

fig1 = px.bar(
    x = category_count.index,
    y = category_count.values,
    labels = {'x':'Category','y':'Count'},
    title = 'Top Categories on Play Store',
    color = category_count.index,
    color_discrete_sequence = px.colors.sequential.Plasma,
    width = plot_width,
    height = plot_height
)

fig1.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    font_color = text_color,
    title_font = title_font,
    xaxis = dict(title_font=axis_font),
    yaxis = dict(title_font=axis_font),
    margin = dict(l=20,r=20,t=50,b=20)
)

fig1.update_traces(marker=dict(line=dict(color=text_color,width=1)))

save_plot_as_html(fig1, "Category Graph 1.html", "The Top Categories on the Play Store are dominated by tools, entertainment, and productivity apps")

#figure 2
type_count = apps_data['Type'].value_counts()

fig2 = px.pie(
    names = type_count.index,
    values = type_count.values,
    title = 'App Type Distribution',
    color_discrete_sequence = px.colors.sequential.RdBu,
    width = plot_width,
    height = plot_height
)

fig2.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    font_color = text_color,
    title_font = title_font,
    margin = dict(l=20,r=20,t=50,b=20)
)

fig2.update_traces(marker=dict(line=dict(color=text_color,width=1)))

save_plot_as_html(fig2, "Type Count 2.html", "Most apps on the Play Store are free, indicating a strategy to attract users first and monetize through ads or in app purchases")

#figure 3
fig3 = px.histogram(
    apps_data,
    x = 'Rating',
    nbins = 50,
    title = 'Rating Distribution',
    color_discrete_sequence = ['#636EFA'],
    width = plot_width,
    height = plot_height
)

fig3.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    title_font = title_font,
    font_color = text_color,
    xaxis = dict(title_font=axis_font),
    yaxis = dict(title_font=axis_font),
    margin = dict(l=20,r=20,t=50,b=20)
)

fig3.update_traces(marker=dict(line=dict(color=text_color,width=1)))

save_plot_as_html(fig3, "Rating Graph 3.html", "Ratings are skewed towards higher values, suggesting most apps are rated favorably by users")

#figure 4
category_installs = apps_data.groupby('Category')['Installs'].sum().nlargest(10)

fig4 = px.bar(
    x = category_installs.index,
    y = category_installs.values,
    labels = {'x':'Category','y':'Installs'},
    title = 'Installs by Category',
    color = category_installs.index,
    color_discrete_sequence = px.colors.sequential.Blues,
    width = plot_width,
    height = plot_height
)

fig4.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    font_color = text_color,
    title_font = title_font,
    xaxis = dict(title_font=axis_font),
    yaxis = dict(title_font=axis_font),
    margin = dict(l=20,r=20,t=50,b=20)
)

fig4.update_traces(marker=dict(line=dict(color=text_color,width=1)))

save_plot_as_html(fig4, "Installs Graph 4.html", "The categories with most installs are social and communication apps, reflecting their board appeal and daily usage")

#figure 5
updates_per_year = apps_data['Year'].value_counts().sort_index()

fig5 = px.line(
    x = updates_per_year.index,
    y = updates_per_year.values,
    labels = {'x':'Year','y':'Number of Counts'},
    title = 'Number of Updates over the Year',
    color_discrete_sequence = ['#AB63FA'],
    width = plot_width,
    height = plot_height
)

fig5.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    font_color = text_color,
    title_font = title_font,
    xaxis = dict(title_font = axis_font),
    yaxis = dict(title_font = axis_font),
    margin = dict(l=20,r=20,t=50,b=20)
)

save_plot_as_html(fig5, "Updates Graph 5.html","Updates have been increasing over the years, showing that developers are actively maintaining and improving their apps")

#figure 6
category_revenue = apps_data.groupby('Category')['Revenue'].sum().nlargest(10)

fig6 = px.bar(
    x = category_revenue.index,
    y = category_revenue.values,
    labels = {'x':'Category','y':'Revenue'},
    title = 'Revenue by Category',
    color = category_revenue.index,
    color_discrete_sequence = px.colors.sequential.Greens,
    width = plot_width,
    height = plot_height
)

fig6.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    font_color = text_color,
    title_font = title_font,
    xaxis = dict(title_font=axis_font),
    yaxis = dict(title_font=axis_font),
    margin = dict(l=20,r=20,t=50,b=20)
)

fig6.update_traces(marker=dict(line=dict(color=text_color,width=1)))

save_plot_as_html(fig6, "Revenue Graph 6.html","Categories such as Business and Productivity lead in revenue generation, indicating their monetization potential")

#figure 7
genres_count = apps_data['Genres'].str.split(';',expand=True).stack().value_counts().nlargest(10)

fig7 = px.bar(
    x = genres_count.index,
    y = genres_count.values,
    labels = {'x':'Genres','y':'Count'},
    title = 'Top Genres',
    color = genres_count.index,
    color_discrete_sequence = px.colors.sequential.OrRd,
    width = plot_width,
    height = plot_height
)

fig7.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    font_color = text_color,
    title_font = title_font,
    xaxis = dict(title_font = axis_font),
    yaxis = dict(title_font = axis_font),
    margin = dict(l=20,r=20,t=50,b=20)
)

fig7.update_traces(marker=dict(line=dict(color=text_color,width=1)))

save_plot_as_html(fig7, "Genres Graph 7.html", "Action and Casual Genres are the most common, reflecting users' preference for engaging and easy to play games")

#figure 8
fig8 = px.scatter(
    apps_data,
    x = 'Last Updated',
    y = 'Rating',
    color = 'Type',
    title = 'Impact of Rating on Last Update',
    color_discrete_sequence = px.colors.qualitative.Vivid,
    width = plot_width,
    height = plot_height
)

fig8.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    font_color = text_color,
    title_font = title_font,
    xaxis = dict(title_font=axis_font),
    yaxis = dict(title_font=axis_font),
    margin = dict(l=20,r=20,t=50,b=20)
)

save_plot_as_html(fig8, "Last Updated Graph 8.html", "The Scatter plot shows a weak correlation between the last update and ratings, suggesting that more frequent updates don't always result in better ratings")

#figure 9
fig9 = px.box(
    apps_data,
    x = 'Type',
    y = 'Rating',
    color = 'Type',
    title = 'Rating for Paid vs Free App',
    color_discrete_sequence = px.colors.qualitative.Pastel,
    width = plot_width,
    height = plot_height
)

fig9.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    font_color = text_color,
    title_font = title_font,
    xaxis = dict(title_font=axis_font),
    yaxis = dict(title_font=axis_font),
    margin = dict(l=20,r=20,t=50,b=20)
)

save_plot_as_html(fig9, "Paid Free Graph 9.html", "Paid apps generally have higher ratings compare to free apps, suggesting that users expect higher quality from apps they pay for")

#figure 10
sentiment_graph = reviews_data['Sentiment_Score'].value_counts()

fig10 = px.bar(
    x = sentiment_graph.index,
    y = sentiment_graph.values,
    labels = {'x':'Sentiment score','y':'Count'},
    title = 'Sentiment Distribution',
    color = sentiment_graph.index,
    color_discrete_sequence = px.colors.sequential.RdPu,
    width = plot_width,
    height = plot_height
)

fig10.update_layout(
    plot_bgcolor = plot_bg_color,
    paper_bgcolor = plot_bg_color,
    font_color = text_color,
    title_font = title_font,
    xaxis = dict(title_font=axis_font),
    yaxis = dict(title_font=axis_font),
    margin = dict(l=20,r=20,t=50,b=20)
)

fig10.update_traces(marker=dict(line=dict(color=text_color,width=1)))

save_plot_as_html(fig10, "Sentiment Score Graph 10.html", "Sentiments in reviews show a mixed of positive and negative feedback, with a slight lean towards positive sentiments")

#figure 11
categories = ['GAME', 'BEAUTY', 'BUSINESS,', 'COMMICS', 'COMMUNICATION', 'DATING', 'ENTERTAINMENT', 'SOCIAL', 'EVENTS']
category_translation = {
    'BEAUTY':'सुंदरता',
    'BUSINESS':'வணிகம்',
    'DATING':'Partnersuche'
}

merged_data = merged_data[
    (merged_data['Rating'] > 3.5) &
    (merged_data['Category'].isin(categories)) &
    (merged_data['Reviews'] > 500) &
    (~merged_data['App'].str.contains('S',case=False,na=False,regex=False)) &
    (merged_data['Sentiment_Subjectivity'] > 0.5) &
    (merged_data['Installs'] > 50000)
].copy()

merged_data['Category_Graph'] = (merged_data['Category'].map(category_translation).fillna(merged_data['Category']))

merged_data['Average_Rating'] = merged_data.groupby('App')['Rating'].transform('mean')

fig11_datetime = pytz.timezone('Asia/Kolkata')
fig11_now = datetime.now(fig11_datetime)

if 17 <= fig11_now.hour < 19:
    fig11 = px.scatter(
        merged_data,
        x = 'Size',
        y = 'Average_Rating',
        size = 'Installs',
        color = 'Category_Graph',
        labels = {'x':'Size','y':'Average_Rating'},
        title = 'Relationship between App Size and Average Rating by Installs',
        width = plot_width,
        height = plot_height,
    )

    fig11.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 13,
        xaxis = dict(title_font=axis_font),
        yaxis = dict(title_font=axis_font),
        margin = dict(l=20,r=20,t=50,b=20)
    )

    for trace in fig11.data:
        if trace.name == 'GAME':
            trace.marker.color = 'pink'

    fig11.update_traces(marker=dict(line=dict(color=text_color,width=1)))

    save_plot_as_html(fig11, "App Size and Average Rating Graph 11.html", "Game category have highest installs means users prefer gaming apps over other apps")

else:
    fig11 = px.scatter(
        title = 'This Chart is available only between 5 PM IST to 7 PM IST',
        width = plot_width,
        height = plot_height
    )
    fig11.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 14
    )

    save_plot_as_html(fig11, "App Size and Average Rating Graph 11.html","Insights available only between 5 PM IST to 7 PM IST")
    
#fig 12
apps_data1 = apps_data

country_keywords = {
    "Afghanistan": ["afghanistan", "afghan"],
    "Albania": ["albania", "albanian"],
    "Algeria": ["algeria", "algerian"],
    "Andorra": ["andorra", "andorran"],
    "Angola": ["angola", "angolan"],
    "Antigua and Barbuda": ["antigua", "barbuda"],
    "Argentina": ["argentina", "argentine", "argentinian"],
    "Armenia": ["armenia", "armenian"],
    "Australia": ["australia", "australian"],
    "Austria": ["austria", "austrian"],
    "Azerbaijan": ["azerbaijan", "azerbaijani"],

    "Bahamas": ["bahamas", "bahamian"],
    "Bahrain": ["bahrain", "bahraini"],
    "Bangladesh": ["bangladesh", "bangladeshi"],
    "Barbados": ["barbados", "barbadian"],
    "Belarus": ["belarus", "belarusian"],
    "Belgium": ["belgium", "belgian"],
    "Belize": ["belize", "belizean"],
    "Benin": ["benin", "beninese"],
    "Bhutan": ["bhutan", "bhutanese"],
    "Bolivia": ["bolivia", "bolivian"],
    "Bosnia and Herzegovina": ["bosnia", "herzegovina", "bosnian"],
    "Botswana": ["botswana", "botswanan"],
    "Brazil": ["brazil", "brazilian"],
    "Brunei": ["brunei", "bruneian"],
    "Bulgaria": ["bulgaria", "bulgarian"],
    "Burkina Faso": ["burkina faso", "burkinabe"],
    "Burundi": ["burundi", "burundian"],

    "Cabo Verde": ["cabo verde", "cape verde", "cape verdean"],
    "Cambodia": ["cambodia", "cambodian"],
    "Cameroon": ["cameroon", "cameroonian"],
    "Canada": ["canada", "canadian"],
    "Central African Republic": ["central african republic"],
    "Chad": ["chad", "chadian"],
    "Chile": ["chile", "chilean"],
    "China": ["china", "chinese"],
    "Colombia": ["colombia", "colombian"],
    "Comoros": ["comoros", "comorian"],
    "Congo": ["congo", "congolese"],
    "Costa Rica": ["costa rica", "costa rican"],
    "Croatia": ["croatia", "croatian"],
    "Cuba": ["cuba", "cuban"],
    "Cyprus": ["cyprus", "cypriot"],
    "Czech Republic": ["czech republic", "czechia", "czech"],

    "Democratic Republic of the Congo": [
        "democratic republic of the congo",
        "dr congo",
        "drc",
        "congo kinshasa"
    ],
    "Denmark": ["denmark", "danish"],
    "Djibouti": ["djibouti", "djiboutian"],
    "Dominica": ["dominica", "dominican"],
    "Dominican Republic": ["dominican republic"],

    "Ecuador": ["ecuador", "ecuadorian"],
    "Egypt": ["egypt", "egyptian"],
    "El Salvador": ["el salvador", "salvadoran"],
    "Equatorial Guinea": ["equatorial guinea"],
    "Eritrea": ["eritrea", "eritrean"],
    "Estonia": ["estonia", "estonian"],
    "Eswatini": ["eswatini", "swazi"],
    "Ethiopia": ["ethiopia", "ethiopian"],

    "Fiji": ["fiji", "fijian"],
    "Finland": ["finland", "finnish"],
    "France": ["france", "french"],

    "Gabon": ["gabon", "gabonese"],
    "Gambia": ["gambia", "gambian"],
    "Georgia": ["georgia", "georgian"],
    "Germany": ["germany", "german"],
    "Ghana": ["ghana", "ghanaian"],
    "Greece": ["greece", "greek"],
    "Grenada": ["grenada", "grenadian"],
    "Guatemala": ["guatemala", "guatemalan"],
    "Guinea": ["guinea", "guinean"],
    "Guinea-Bissau": ["guinea-bissau", "guinea bissau"],
    "Guyana": ["guyana", "guyanese"],

    "Haiti": ["haiti", "haitian"],
    "Honduras": ["honduras", "honduran"],
    "Hungary": ["hungary", "hungarian"],

    "Iceland": ["iceland", "icelandic"],
    "India": ["india", "indian"],
    "Indonesia": ["indonesia", "indonesian"],
    "Iran": ["iran", "iranian", "persian"],
    "Iraq": ["iraq", "iraqi"],
    "Ireland": ["ireland", "irish"],
    "Israel": ["israel", "israeli"],
    "Italy": ["italy", "italian"],
    "Ivory Coast": ["ivory coast", "cote d'ivoire", "ivorian"],

    "Jamaica": ["jamaica", "jamaican"],
    "Japan": ["japan", "japanese"],
    "Jordan": ["jordan", "jordanian"],

    "Kazakhstan": ["kazakhstan", "kazakh"],
    "Kenya": ["kenya", "kenyan"],
    "Kiribati": ["kiribati"],
    "Kuwait": ["kuwait", "kuwaiti"],
    "Kyrgyzstan": ["kyrgyzstan", "kyrgyz"],

    "Laos": ["laos", "laotian", "lao"],
    "Latvia": ["latvia", "latvian"],
    "Lebanon": ["lebanon", "lebanese"],
    "Lesotho": ["lesotho", "basotho"],
    "Liberia": ["liberia", "liberian"],
    "Libya": ["libya", "libyan"],
    "Liechtenstein": ["liechtenstein"],
    "Lithuania": ["lithuania", "lithuanian"],
    "Luxembourg": ["luxembourg", "luxembourgish"],

    "Madagascar": ["madagascar", "malagasy"],
    "Malawi": ["malawi", "malawian"],
    "Malaysia": ["malaysia", "malaysian"],
    "Maldives": ["maldives", "maldivian"],
    "Mali": ["mali", "malian"],
    "Malta": ["malta", "maltese"],
    "Marshall Islands": ["marshall islands"],
    "Mauritania": ["mauritania", "mauritanian"],
    "Mauritius": ["mauritius", "mauritian"],
    "Mexico": ["mexico", "mexican"],
    "Micronesia": ["micronesia", "micronesian"],
    "Moldova": ["moldova", "moldovan"],
    "Monaco": ["monaco", "monegasque"],
    "Mongolia": ["mongolia", "mongolian"],
    "Montenegro": ["montenegro", "montenegrin"],
    "Morocco": ["morocco", "moroccan"],
    "Mozambique": ["mozambique", "mozambican"],
    "Myanmar": ["myanmar", "burma", "burmese"],

    "Namibia": ["namibia", "namibian"],
    "Nauru": ["nauru", "nauruan"],
    "Nepal": ["nepal", "nepalese"],
    "Netherlands": ["netherlands", "dutch", "holland"],
    "New Zealand": ["new zealand", "new zealander"],
    "Nicaragua": ["nicaragua", "nicaraguan"],
    "Niger": ["niger", "nigerien"],
    "Nigeria": ["nigeria", "nigerian"],
    "North Korea": ["north korea", "north korean"],
    "North Macedonia": ["north macedonia", "macedonian"],
    "Norway": ["norway", "norwegian"],

    "Oman": ["oman", "omani"],

    "Pakistan": ["pakistan", "pakistani"],
    "Palau": ["palau", "palauan"],
    "Panama": ["panama", "panamanian"],
    "Papua New Guinea": ["papua new guinea"],
    "Paraguay": ["paraguay", "paraguayan"],
    "Peru": ["peru", "peruvian"],
    "Philippines": ["philippines", "filipino", "filipina"],
    "Poland": ["poland", "polish"],
    "Portugal": ["portugal", "portuguese"],

    "Qatar": ["qatar", "qatari"],

    "Romania": ["romania", "romanian"],
    "Russia": ["russia", "russian"],
    "Rwanda": ["rwanda", "rwandan"],

    "Saint Kitts and Nevis": ["saint kitts", "nevis"],
    "Saint Lucia": ["saint lucia"],
    "Saint Vincent and the Grenadines": ["saint vincent", "grenadines"],
    "Samoa": ["samoa", "samoan"],
    "San Marino": ["san marino"],
    "Sao Tome and Principe": ["sao tome", "principe"],
    "Saudi Arabia": ["saudi arabia", "saudi"],
    "Senegal": ["senegal", "senegalese"],
    "Serbia": ["serbia", "serbian"],
    "Seychelles": ["seychelles", "seychellois"],
    "Sierra Leone": ["sierra leone"],
    "Singapore": ["singapore", "singaporean"],
    "Slovakia": ["slovakia", "slovak"],
    "Slovenia": ["slovenia", "slovenian"],
    "Solomon Islands": ["solomon islands"],
    "Somalia": ["somalia", "somali"],
    "South Africa": ["south africa", "south african"],
    "South Korea": ["south korea", "south korean", "korea"],
    "South Sudan": ["south sudan", "south sudanese"],
    "Spain": ["spain", "spanish"],
    "Sri Lanka": ["sri lanka", "sri lankan"],
    "Sudan": ["sudan", "sudanese"],
    "Suriname": ["suriname", "surinamese"],
    "Sweden": ["sweden", "swedish"],
    "Switzerland": ["switzerland", "swiss"],
    "Syria": ["syria", "syrian"],

    "Taiwan": ["taiwan", "taiwanese"],
    "Tajikistan": ["tajikistan", "tajik"],
    "Tanzania": ["tanzania", "tanzanian"],
    "Thailand": ["thailand", "thai"],
    "Timor-Leste": ["timor-leste", "east timor"],
    "Togo": ["togo", "togolese"],
    "Tonga": ["tonga", "tongan"],
    "Trinidad and Tobago": ["trinidad", "tobago"],
    "Tunisia": ["tunisia", "tunisian"],
    "Turkey": ["turkey", "turkish"],
    "Turkmenistan": ["turkmenistan", "turkmen"],
    "Tuvalu": ["tuvalu", "tuvaluan"],

    "Uganda": ["uganda", "ugandan"],
    "Ukraine": ["ukraine", "ukrainian"],
    "United Arab Emirates": ["united arab emirates", "uae", "emirates"],
    "United Kingdom": ["united kingdom", "uk", "britain", "british", "england", "london"],
    "United States": ["united states", "usa", "america", "american", "us"],
    "Uruguay": ["uruguay", "uruguayan"],
    "Uzbekistan": ["uzbekistan", "uzbek"],

    "Vanuatu": ["vanuatu", "vanuatuan"],
    "Vatican City": ["vatican", "holy see"],
    "Venezuela": ["venezuela", "venezuelan"],
    "Vietnam": ["vietnam", "vietnamese"],

    "Yemen": ["yemen", "yemeni"],

    "Zambia": ["zambia", "zambian"],
    "Zimbabwe": ["zimbabwe", "zimbabwean"]
}

def detect_country(app_name):
    app_name = str(app_name).lower()
    for country, keywords in country_keywords.items():
        for keyword in keywords:
            if keyword in app_name:
                return country
    return "Unknown"

apps_data1['Country'] = apps_data1['App'].apply(detect_country)
apps_data1 = apps_data1[
    (apps_data1['Installs'] > 1000000) &
    (~apps_data1['Category'].astype(str).str.startswith(('A','C','G','S'),na=False))
].copy()

apps_data1 = apps_data1.groupby(['Category','Country'])['Installs'].sum().nlargest(5).reset_index()
apps_data1['Highlight'] = apps_data1['Installs'].apply(
    lambda x: "Above 1 Million" if x > 1000000 else "Below 1 Million"
)

fig12_datetime = pytz.timezone('Asia/Kolkata')
fig12_now = datetime.now(fig12_datetime)

if 18 <= fig12_now.hour < 20:
    fig12 = px.choropleth(
        apps_data1,
        locations = 'Country',
        locationmode = 'country names',
        color = 'Installs',
        hover_name = 'Country',
        title = 'Global App Installs by Category - Top 5 Categories',
        animation_frame = 'Category',
        color_continuous_scale = 'Viridis'
    )

    fig12.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        width = plot_width,
        height = plot_height,
        xaxis = dict(title_font=axis_font),
        yaxis = dict(title_font=axis_font)
    )

    fig12.update_coloraxes(
        colorbar_title = 'Installs exceeds 1 Million'
    )

    save_plot_as_html(fig12, "Global Top 5 Categories 12.html", "The name of the countries are unknown as the country column does not show any particular country name but all the categories involved over 1 Million installs")

else:
    fig12 = px.scatter(
        title = 'This Chart is available only between 6 PM IST to 8 PM IST',
        width = plot_width,
        height = plot_height
    )
    fig12.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 14
    )

    save_plot_as_html(fig12, "Choropleth Graph 12.html","Insights available only between 6 PM IST to 8 PM IST")
    
#fig 13
apps_data2 = apps_data

category_translation1 = {
    'BEAUTY':'सुंदरता',
    'BUSINESS':'வணிகம்',
    'DATING':'Partnersuche'
}

apps_data2 = apps_data2[
    (~apps_data2['App'].str.startswith(('x','y','z'),na=False)) &
    (apps_data2['Category'].str.startswith(('E','C','B'),na=False)) &
    (apps_data2['Reviews'] > 500) &
    (apps_data2['App'].str.contains('S',case=False,na=False,regex=False))
].copy()

apps_data2['Category_Graph'] = apps_data2['Category'].map(category_translation1).fillna(apps_data2['Category'])
apps_data2['Month'] = apps_data2['Last Updated'].dt.to_period('M').dt.to_timestamp()
apps_data2 = (apps_data2.groupby(['Month','Category_Graph']).agg(Total_Installs=('Installs','sum')).reset_index())
apps_data2['Growth'] = apps_data2['Total_Installs'].pct_change()*100
growth = apps_data2[apps_data2['Growth'] > 20]

fig13_datetime = pytz.timezone('Asia/Kolkata')
fig13_now = datetime.now(fig13_datetime)

if 18 <= fig13_now.hour < 21:
    fig13 = px.line(
        growth,
        x = 'Month',
        y = 'Total_Installs',
        color = 'Category_Graph',
        title = 'Total Installs over Time (20% Growth)',
        width = plot_width,
        height = plot_height
    )

    fig13.add_scatter(
        x = growth['Month'],
        y = growth['Total_Installs'],
        mode = 'markers',
        marker = dict(size=4,color='yellow'),
        name = 'Growth > 20%'
    )

    fig13.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 16,
        xaxis = dict(title_font=axis_font),
        yaxis = dict(title_font=axis_font)
    )
    save_plot_as_html(fig13, "Total Installs over Time 13.html", "Growth is highest between Aug 2017 to Sep 2018, otherwise the total installs are almost maintain the same line")

else:
    fig13 = px.scatter(
        title = 'This Chart is available only between 6 PM IST to 9 PM IST',
        width = plot_width,
        height = plot_height
    )
    fig13.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 14
    )
    save_plot_as_html(fig13, "Total Installs over Time 13.html", "Insights are available only between 6 PM IST to 9 PM IST")
    
#fig 14
apps_data3 = apps_data

category_translation2 = {
    'TRAVEL_AND_LOCAL':'Voyages et local',
    'PRODUCTIVITY':'Productividad',
    'PHOTOGRAPHY':'写真'
}

apps_data3 = apps_data3[
    (apps_data3['Rating'] >= 4.2) &
    (~apps_data3['App'].str.contains(r'/d',case=False,na=False,regex=False)) &
    (apps_data3['Category'].str.startswith(('T','P'),na=False)) &
    (apps_data3['Reviews'] > 1000) &
    ((apps_data3['Size'] > 20) & (apps_data3['Size'] < 80))
].copy()

apps_data3['Category Graph'] = (apps_data3['Category'].map(category_translation2).fillna(apps_data3['Category']))
apps_data3['Month'] = apps_data3['Last Updated'].dt.to_period('M').dt.to_timestamp()
apps_data3['Cumulative Installs'] = (apps_data3.groupby('Category Graph')['Installs'].cumsum())
apps_data3['Average Rating'] = apps_data3['Rating'].mean()
growth1 = apps_data3.groupby(['Month','Category Graph'])['Cumulative Installs'].sum().reset_index()
growth1 = growth1.sort_values(['Month','Cumulative Installs'])
growth1['Growth'] = (growth1.groupby('Category Graph')['Cumulative Installs'].pct_change()*100)
growth1 = growth1[growth1['Cumulative Installs'] > 25]

fig14_datetime = pytz.timezone('Asia/Kolkata')
fig14_now = datetime.now(fig14_datetime)

if 16 <= fig14_now.hour < 18:
    fig14 = px.area(
        growth1,
        x = 'Month',
        y = 'Cumulative Installs',
        color = 'Category Graph',
        title = 'Cumulative number of Installs over Time (25% Growth)',
        width = plot_width,
        height = plot_height
    )

    fig14.add_scatter(
        x = growth1['Month'],
        y = growth1['Cumulative Installs'],
        mode = 'markers',
        marker = dict(size=4,color='yellow'),
        name = 'Growth > 25%'
    )

    fig14.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 15,
        xaxis = dict(title_font=axis_font),
        yaxis = dict(title_font=axis_font)
    )
    save_plot_as_html(fig14, "Cumulative Installs over Time 14.html", "The Stacked Area Chart represents that the average rating is 4.4 and reviews greater than 1000")
else:
    fig14 = px.scatter(
        title = 'This Chart is available only between 4 PM IST to 6 PM IST',
        width = plot_width,
        height = plot_height
    )
    fig14.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 14
    )
    save_plot_as_html(fig14, "cumulative Installs over Time 14.html", "Insights are available only between 4 PM IST to 6 PM IST")
    
#fig 15
apps_data4 = apps_data
apps_data4['Month'] = apps_data4['Last Updated'].dt.month_name()

apps_data4 = apps_data4[
    (apps_data4['Rating'] >= 4.0) &
    (apps_data4['Size'] >= 10) &
    (apps_data4['Month'] == 'January')
].copy()

category_bar = apps_data4.groupby('Category')['Installs'].sum().nlargest(10).index
apps_data4 = apps_data4[apps_data4['Category'].isin(category_bar)].copy()
apps_data4 = (apps_data4.groupby(['Category']).agg(Average_Rating = ('Rating','mean'),
                                                   Total_Installs = ('Installs','sum'),
                                                   Total_Reviews = ('Reviews','sum')).reset_index())

apps_data4 = apps_data4.melt(
    id_vars = 'Category',
    value_vars = ['Average_Rating','Total_Reviews'],
    var_name = 'Metric',
    value_name = 'Value'
)

apps_data4['Normalized Data'] = apps_data4.groupby('Metric')['Value'].transform(lambda x: (x/x.max())*100)

fig15_datetime = pytz.timezone('Asia/Kolkata')
fig15_now = datetime.now(fig15_datetime)

if 15 <= fig15_now.hour < 17:
    fig15 = px.bar(
        apps_data4,
        x = 'Category',
        y = 'Normalized Data',
        color = 'Metric',
        barmode = 'group',
        title = 'Comparison of Average Rating and Total Review Count',
        width = plot_width,
        height = plot_height
    )

    fig15.update_layout(
        yaxis_title = 'Normalized Value (%)',
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 14,
        xaxis = dict(title_font=axis_font),
        yaxis = dict(title_font=axis_font),
        margin = dict(l=20,r=20,t=50,b=20)
    )

    fig15.update_traces(marker=dict(line=dict(color=text_color,width=1)))
    save_plot_as_html(fig15, "Average Rating and Total Review Count 15.html", "Both Average Rating and Total Review Count are in Percentage format, where Rating is > 4.0 and time indicates only January month")
else:
    fig15 = px.scatter(
        title = 'This Chart is available only between 3 PM IST to 5 PM IST',
        width = plot_width,
        height = plot_height
    )
    fig15.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 14
    )
    save_plot_as_html(fig15, "Average Rating and Total Review Count 15.html", "Insights are available only between 3 PM IST to 5 PM IST")
    
#fig 16
apps_data5 = apps_data

apps_data5['Android Ver'] = apps_data5['Android Ver'].astype(str).str.replace('and up','')
apps_data5['Android Ver'] = apps_data5['Android Ver'].str.replace('Varies with device','')
apps_data5['Android Ver'] = apps_data5['Android Ver'].str.replace(' ','')
apps_data5['Android Ver'] = pd.to_numeric(apps_data5['Android Ver'],errors='coerce')

apps_data5 = apps_data5[
    (apps_data5['Installs'] >= 10000) &
    (apps_data5['Revenue'] >= 10000) &
    (apps_data5['Android Ver'] > 4.0) &
    (apps_data5['Size'] > 15) &
    (apps_data5['Content Rating'] == 'Everyone') &
    (apps_data5['App'].astype(str).str.len() <= 30)
].reset_index()

dual_axis = apps_data5.groupby('Category')['Installs'].sum().nlargest(3).index
apps_data5 = apps_data5[apps_data5['Category'].isin(dual_axis)].copy()
apps_data5 = (apps_data5.groupby(['Category','Type']).agg(Average_Installs=('Installs','mean'),
                                                        Average_Revenue=('Revenue','mean')).reset_index())

fig16_datetime = pytz.timezone('Asia/Kolkata')
fig16_now = datetime.now(fig16_datetime)

if 13 <= fig16_now.hour < 14:
    fig16 = go.Figure()

    fig16.add_trace(
        go.Bar(
            x = apps_data5['Category'],
            y = apps_data5['Average_Installs'],
            offsetgroup = 'installs',
            customdata = apps_data5['Type'],
            hovertemplate = 'Type: %{customdata}<br>' + 'Average Installs: %{y}<extra></extra>',
            marker = {'color':'blue'},
            name = 'Average Installs',
            yaxis = 'y'
        )
    )

    fig16.add_trace(
        go.Bar(
            x = apps_data5['Category'],
            y = apps_data5['Average_Revenue'],
            offsetgroup = 'revenue',
            customdata = apps_data5['Type'],
            hovertemplate = 'Type: %{customdata}<br>' + 'Average Revenue: %{y}<extra></extra>',
            marker = {'color':'green'},
            name = 'Average Revenue',
            yaxis = 'y2'
        )
    )

    fig16.update_layout(
        title = 'Average Installs and Average Revenue: Free vs Paid Apps',
        xaxis_title = 'Category',
        yaxis = dict(title='Average Installs'),
        yaxis2 = dict(title='Average Revenue',overlaying='y',side='right'),
        barmode = 'group',
        legend = dict(orientation='h',xanchor='right'),
        title_font = {'size':14},
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        margin = dict(l=20,r=20,t=50,b=20),
        width = plot_width,
        height = plot_height
    )

    fig16.update_traces(marker=dict(line=dict(color=text_color,width=1)))

    save_plot_as_html(fig16, "Average Installs and Average Revenue 16.html", "Maximum users show that they preferred paid apps over Free Apps in case of Installs and Revenue, thus we don't find any Free Apps")
else:
    fig16 = px.scatter(
        title = 'This Chart is available only between 1 PM IST to 2 PM IST',
        width = plot_width,
        height = plot_height
    )
    fig16.update_layout(
        plot_bgcolor = plot_bg_color,
        paper_bgcolor = plot_bg_color,
        font_color = text_color,
        title_font = title_font,
        title_font_size = 14
    )
    save_plot_as_html(fig16, "Average Installs and Average Revenue 16.html", "Insights are available only between 1 PM IST to 2 PM IST")