import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import tools
import math

# https://htmlcheatsheet.com/css/

######################################################Data##############################################################

df = pd.read_excel('Pasta1.xlsx')

######################################################Colors#############################################################

color_array = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", '#9a6a00',
                   '#0047e6','#00523b', '#893c00']

color_line = ['#2b8cbe', '#e34a33','#31a354','#756bb1','#636363','#93003a']

color_bar = ['#a6bddb','#fdbb84','#a1d99b','#bcbddc','#bdbdbd',' #ff005e']

color_accum = ['rgba(166,189,219,0.5)', 'rgba(253,187,132,0.5)', 'rgba(161,217,155,0.5)','rgba(188,189,220,0.5)',
               'rgba(189,189,189,0.5)','rgba(255,0,94,0.5)']

Europe = ['Albania','Austria','Armenia','Azerbaijan','Belarus','Belgium','Bosnia and Herzegovina','Bulgaria','Croatia',
          'Cyprus','Czechia','Denmark','Estonia','Finland','France','Georgia','Germany','Greece','Hungary','Iceland',
          'Ireland','Italy','Kazakhstan','Latvia','Lithuania','Luxembourg','Netherlands','Norway','Malta','Moldova',
          'Poland','Portugal','Romania','Ukraine','Russian Federation','Slovakia','Slovenia','Spain','Sweden',
          'Switzerland','Turkey','United Kingdom of Great Britain and Northern Ireland']

list=df['GeoAreaName'].unique()
####################################################Options#############################################################

country_options = [
    dict(label='Country ' + country, value=country)
    for country in df['GeoAreaName'][(df['SeriesDescription']=='International financial flows to developing countries in support of clean energy research and development and renewable energy production, including in hybrid systems (millions of constant 2016 United States dollars)')].unique()]

allcountry_options = [
    dict(label='Country ' + country, value=country)
    for country in df['GeoAreaName'][(df['SeriesDescription']=='Proportion of population with primary reliance on clean fuels and technology (%)')].unique()]

map_options = [
    {'label': 'World', 'value': 'World'},
    {'label': 'Europe', 'value': 'Europe'}]

dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Brazil'],
        multi=True)

dropdown_allcountry = dcc.Dropdown(
        id='allcountry_drop',
        options=allcountry_options,
        value=['Brazil'],
        multi=True)

radio_map = dcc.RadioItems(
        id='map_radio',
        options=map_options,
        value='Europe')
        #labelStyle={'display': 'inline'})

year_slider = dcc.RangeSlider(
        id='year_slider',
        min=2003,
        max=2017,
        value=[2003, 2017],
        marks={'2003': '2003',
               '2005': '2005',
               '2007': '2007',
               '2009': '2009',
               '2011': '2011',
               '2013': '2013',
               '2015': '2015',
               '2017': '2017'},
        step=1)

allyear_slider = dcc.RangeSlider(
        id='allyear_slider',
        min=2003,
        max=2017,
        value=[2003, 2017],
        marks={'2003': '2003',
               '2005': '2005',
               '2007': '2007',
               '2009': '2009',
               '2011': '2011',
               '2013': '2013',
               '2015': '2015',
               '2017': '2017'},
        step=1)


######################################################App###############################################################

app = dash.Dash(__name__, external_stylesheets='')

app.layout = html.Div([

    html.H1('SUSTAINABLE DEVELOPMENT GOALS'),
    html.H3('United Nations Global SDG Indicators'),
    html.H3('GOALS 7, 9 AND 12'),
    html.H5('Goal 7 -  Ensure access to affordable, reliable, sustainable and modern energy for all'),
    html.H5('Goal 9 - Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation'),
    html.H5('Goal 12 - Ensure sustainable consumption and production patterns'),

html.Div([
html.Div([
            dropdown_allcountry,

                    ], style={'width': '50%'}),

html.Div([
            allyear_slider,

                     ], style={'width': '50%'})
], style={'display': 'flex'}, className='pretty'),


html.Div([
html.Div([
            dcc.Graph(id='graph_line_bar')
        ],style={'width': '80%'} ),
html.Div([
            dcc.Markdown('''###### Target 7.1: Ensure universal access to affordable, reliable and modern energy services by 2030.'''),
            dcc.Markdown('''###### Indicator 7.1.1: Proportion of population with access to electricity (bars)'''),
            dcc.Markdown('''###### Indicator 7.1.2: Proportion of population with primary reliance on clean fuels and technology (lines)'''
                         )
        ],style={'width': '20%'} ),
], style={'display': 'flex'}, className='pretty'),


html.Div([
html.Div([
            dcc.Graph(id='graph_line')
], style={'width': '80%'}),
    html.Div([
        dcc.Markdown('''###### Target 7.2: Increase substantially the share of renewable energy in the global energy mix by 2030.'''),
        dcc.Markdown('''###### Indicator 7.2.1: Renewable energy share in the total final energy consumption'''),

    ], style={'width': '20%'}),
], style={'display': 'flex'}, className='pretty'),

html.Div([
html.Div([

        html.Div([
        dcc.Markdown('''###### Target 7.3: Double the global rate of improvement in energy efficiency by 2030.'''),
        dcc.Markdown('''###### Indicator 7.3.1: Energy intensity measured in terms of primary energy and GDP'''),
        dcc.Markdown('''###### Choose a map:'''),
        radio_map

    ], style={'text-align': 'center','width': '100%'}),

]),


html.Div([
    html.Div([
        dcc.Graph(id='choropleth'),
        dcc.Graph(id='choropleth2'),
        ], style={'text-align': 'center'}),
]),
], className='pretty'),


html.Div([
html.Div([
            dcc.Graph(id='graph_bubble2')
], style={'width': '80%'}),
    html.Div([
        dcc.Markdown('''###### Target 9.5: Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, in particular developing countries, including, by 2030'''),
        dcc.Markdown('''###### Indicator 9.5.1: Research and development expenditure as a proportion of GDP'''),
        dcc.Markdown('''###### Indicator 9.5.2: Researchers (in full-time equivalent) per million inhabitants'''),

    ], style={'width': '20%'}),
], style={'display': 'flex'}, className='pretty'),

html.Div([
html.Div([
            dcc.Graph(id='dots')
        ],style={'width': '80%'}),

html.Div([
        dcc.Markdown('''###### Target 12.1: Implement the 10-Year Framework of Programmes on Sustainable Consumption and Production Patterns, all countries taking action, with developed countries taking the lead, taking into account the development and capabilities of developing countries'''),
        dcc.Markdown('''###### Indicator 12.1.1: Countries with policy instrument for sustainable consumption and production'''),

    ], style={'width': '20%'}),
        ],style={'display': 'flex'},className='pretty'),

html.Div([
    html.H3('International Cooperation to aid Developing Countries'),
    html.H6('The visualization created aims to help to understand how the international financial aid influenced indicator 7.2.1 developed to measure Goal 7.'),
    ],className='pretty'),

html.Div([
html.Div([
            dropdown_country,

                    ], style={'width': '50%'}),

html.Div([
            year_slider,

                     ], style={'width': '50%'})
], style={'display': 'flex'},className='pretty'),


html.Div([
html.Div([
           dcc.Graph(id='accum')
            ],style={'width': '80%'}),
html.Div([
        dcc.Markdown('''###### Target 7.a: Enhance international cooperation to facilitate access to clean energy research and technology, including renewable energy, energy efficiency and advanced and cleaner fossil-fuel technology, and promote investment in energy infrastructure and clean energy technology, by 2030'''),
        dcc.Markdown('''###### Indicator 7.a.1: International financial flows to developing countries in support of clean energy research and development and renewable energy production, including in hybrid systems'''),


    ], style={'width': '20%'}),
], style={'display': 'flex'}, className='pretty'),


])

######################################################Callback##########################################################

@app.callback(
    [Output("choropleth", "figure"),
     Output("choropleth2", "figure"),
     Output("graph_line", "figure"),
     Output("graph_line_bar", "figure"),
     Output("graph_bubble2", "figure"),
     Output('accum', 'figure'),
     Output('dots', 'figure')],
    [Input('country_drop', 'value'),
     Input('year_slider', 'value'),
     Input('allcountry_drop', 'value'),
     Input('allyear_slider', 'value'),
     Input('map_radio', 'value')]
)
def update_graph(countries, year, allcountries, allyear, map):
    filtered_by_year_df = df[(df['TimePeriod'] >= year[0]) & (df['TimePeriod'] <= year[1])]
    filtered_by_year_and_country_df = filtered_by_year_df[filtered_by_year_df['GeoAreaName'].isin(countries)].sort_values(by='TimePeriod')
    filtered_by_allyear_df = df[(df['TimePeriod'] >= allyear[0]) & (df['TimePeriod'] <= allyear[1])]
    filtered_by_allyear_and_allcountry_df = filtered_by_allyear_df[filtered_by_allyear_df['GeoAreaName'].isin(allcountries)].sort_values(by='TimePeriod')

######################################################Choropleth########################################################



    df_EU = df[df['GeoAreaName'].isin(Europe)]
    df_EU_0 = df_EU[(df_EU['TimePeriod'] == 2003) & (df_EU['SeriesDescription'] == 'Energy intensity level of primary energy (megajoules per constant 2011 purchasing power parity GDP)')]

    df_all = df[df['GeoAreaName'].isin(list)]
    df_all_0 = df_all[(df_all['TimePeriod'] == 2003) & (df_all['SeriesDescription'] == 'Energy intensity level of primary energy (megajoules per constant 2011 purchasing power parity GDP)')]

    if map == 'Europe':
        data_choropleth = dict(type='choropleth',
                               locations=df_EU_0['GeoAreaName'],
                               locationmode='country names',
                               text=df_EU_0['GeoAreaName'],
                               colorscale='YlGnBu',
                               autocolorscale=False,
                               zmax=30,
                               zmin=0,
                               colorbar=dict(title='megajoules per constant <br> 2011 purchasing power parity GDP'),
                               z=df_EU_0['Value'])

        layout_choropleth = dict(geo=dict(scope='europe',
                                      projection={'type': 'equirectangular'},
                                      bgcolor='#f9f9f9',
                                      showframe=False
                                      ),
                             title=dict(text='2003',
                                        x=.5,
                                        # Title relative position according to the xaxis, range (0,1)
                                        ),
                             font=dict(size=12, color="#4d4d4d"),
                             paper_bgcolor='#f9f9f9')
    if map == 'World':
        data_choropleth = dict(type='choropleth',
                               locations=df_all_0['GeoAreaName'],
                               locationmode='country names',
                               text=df_all_0['GeoAreaName'],
                               colorscale='YlGnBu',
                               autocolorscale=False,
                               zmax=30,
                               zmin=0,
                               colorbar=dict(title='megajoules per constant <br> 2011 purchasing power parity GDP'),
                               z=df_all_0['Value'])

        layout_choropleth = dict(geo=dict(#scope='europe',
                                          projection={'type': 'equirectangular'},
                                          bgcolor='#f9f9f9',
                                          showframe=False
                                          ),
                                 title=dict(text='2003',
                                            x=.5,
                                            # Title relative position according to the xaxis, range (0,1)
                                            ),
                                 font=dict(size=12, color="#4d4d4d"),
                                 paper_bgcolor='#f9f9f9')

######################################################Choropleth2########################################################

    df_EU_1 = df_EU[(df_EU['TimePeriod'] == 2017) & (df_EU[
                                                         'SeriesDescription'] == 'Energy intensity level of primary energy (megajoules per constant 2011 purchasing power parity GDP)')]
    df_all_1 = df_all[(df_all['TimePeriod'] == 2017) & (df_all[
                                                            'SeriesDescription'] == 'Energy intensity level of primary energy (megajoules per constant 2011 purchasing power parity GDP)')]


    if map == 'Europe':
            data_choropleth2 = dict(type='choropleth',
                                   locations=df_EU_1['GeoAreaName'],
                                   locationmode='country names',
                                   text=df_EU_1['GeoAreaName'],
                                   colorscale='YlGnBu',
                                   autocolorscale=False,
                                    zmax=30,
                                    zmin=0,
                                   colorbar=dict(title='megajoules per constant <br> 2011 purchasing power parity GDP'),
                                   z=df_EU_1['Value'])

            layout_choropleth2 = dict(geo=dict(scope='europe',
                                              projection={'type': 'equirectangular'},
                                              bgcolor='#f9f9f9',
                                              showframe=False
                                              ),
                                     title=dict(
                                         text='2017',
                                         x=.5,
                                         # Title relative position according to the xaxis, range (0,1)
                                         ),
                                     font=dict(size=12, color="#4d4d4d"),
                                     paper_bgcolor='#f9f9f9')
    if map == 'World':
            data_choropleth2 = dict(type='choropleth',
                                   locations=df_all_1['GeoAreaName'],
                                   locationmode='country names',
                                   text=df_all_1['GeoAreaName'],
                                   colorscale='YlGnBu',
                                   autocolorscale=False,
                                   zmax=30,
                                   zmin=0,
                                   colorbar=dict(title='megajoules per constant <br> 2011 purchasing power parity GDP'),
                                   z=df_all_1['Value'])

            layout_choropleth2 = dict(geo=dict(  # scope='europe',
                projection={'type': 'equirectangular'},
                bgcolor='#f9f9f9',
                showframe=False
            ),
                title=dict(
                    text='2017',
                    x=.5,
                    # Title relative position according to the xaxis, range (0,1)
                    ),
                font=dict(size=12, color="#4d4d4d"),
                paper_bgcolor='#f9f9f9')

    ######################################################LayoutLine########################################################

    color_numb1=0
    data_line1 = []
    for country in allcountries:
            data_line1.append(dict(type='scatter',
                               x=filtered_by_allyear_and_allcountry_df['TimePeriod'][(filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Renewable energy share in the total final energy consumption (%)') & (filtered_by_allyear_and_allcountry_df['GeoAreaName'] == country)],
                               y=filtered_by_allyear_and_allcountry_df['Value'][(filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Renewable energy share in the total final energy consumption (%)') & (filtered_by_allyear_and_allcountry_df['GeoAreaName'] == country)],
                               name=country,
                               line_color=color_line[color_numb1]
                               ))
            color_numb1 += 1

    layout_line = dict(title=dict(text='Indicator 7.2.1', x=0.5),
                       yaxis=dict(title='Renewable energy share (%)',range=[0, 100]),
                       paper_bgcolor='#f9f9f9',
                       template='none',
                       font=dict(size=12, color="#4d4d4d"),
                       legend=dict(orientation='h', yanchor='top', xanchor='center', y=-0.3, x=0.5))

####################################################LayoutLineBar#######################################################

    color_numb2=0
    data_line_bar=[]
    for country in allcountries:
            data_line_bar.append(dict(type='bar',
                               x=filtered_by_allyear_and_allcountry_df['TimePeriod'][(filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Proportion of population with access to electricity, by urban/rural (%)') & (filtered_by_allyear_and_allcountry_df['GeoAreaName'] == country) & (filtered_by_allyear_and_allcountry_df['Location']=='ALLAREA')],
                               y=filtered_by_allyear_and_allcountry_df['Value'][(filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Proportion of population with access to electricity, by urban/rural (%)') & (filtered_by_allyear_and_allcountry_df['GeoAreaName']==country) & (filtered_by_allyear_and_allcountry_df['Location']=='ALLAREA')],
                               legendgroup=country,
                               name=country + ' - Access to electricity',
                               marker_color=color_bar[color_numb2]
                               ))
            color_numb2 +=1

    color_numb3=0
    for country in allcountries:
            data_line_bar.append(dict(type='scatter',
                               x=filtered_by_allyear_and_allcountry_df['TimePeriod'][(filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Proportion of population with access to electricity, by urban/rural (%)') & (filtered_by_allyear_and_allcountry_df['GeoAreaName'] == country) & (filtered_by_allyear_and_allcountry_df['Location']=='ALLAREA')],
                               y=filtered_by_allyear_and_allcountry_df['Value'][(filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Proportion of population with primary reliance on clean fuels and technology (%)') & (filtered_by_allyear_and_allcountry_df['GeoAreaName']==country)],
                               legendgroup=country,
                               name =country + ' - Primary reliance on clean fuels and technology',
                               line_color=color_line[color_numb3]
                               ))
            color_numb3 +=1


    layout_line_bar = dict(title=dict(text='Indicators 7.1.1 and 7.1.2', x=0.5),
                       yaxis=dict(title='Proportion of population (%)'),
                       paper_bgcolor='#f9f9f9',
                       template='none',
                       font=dict(size=12, color="#4d4d4d"),
                       legend=dict(orientation='h', yanchor='top', xanchor='center', y=-0.3, x=0.5))

######################################################Bubble All########################################################

    filtered_by_allyear_and_allcountry_df.sort_values(by=['GeoAreaName', 'TimePeriod'], inplace=True)
    data_bubble2 = px.scatter(x=filtered_by_allyear_and_allcountry_df['Value'][filtered_by_allyear_and_allcountry_df[
                                                                                   'SeriesDescription'] == 'Research and development expenditure as a proportion of GDP (%)'],
                              y=filtered_by_allyear_and_allcountry_df['Value'][filtered_by_allyear_and_allcountry_df[
                                                                                   'SeriesDescription'] == 'Researchers (in full-time equivalent) per million inhabitants (per 1,000,000 population)'],
                              animation_frame=filtered_by_allyear_and_allcountry_df['TimePeriod'][filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Research and development expenditure as a proportion of GDP (%)'],
                              animation_group=filtered_by_allyear_and_allcountry_df['GeoAreaName'][filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Research and development expenditure as a proportion of GDP (%)'],
                              hover_name=filtered_by_allyear_and_allcountry_df['GeoAreaName'][filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Research and development expenditure as a proportion of GDP (%)'],
                              color=filtered_by_allyear_and_allcountry_df['GeoAreaName'][filtered_by_allyear_and_allcountry_df['SeriesDescription'] == 'Research and development expenditure as a proportion of GDP (%)'])

    data_bubble2.update_traces(hovertemplate='GPD expenditure in research: %{x} % <br>Researchers: %{y} per million inhabitants')

    layout_bubble2 = data_bubble2.update_layout(title=dict(text="Indicators 9.5.1 and 9.5.2",x=0.5),
                                              xaxis=dict(
                                                  title='Research and development expenditure as a proportion of GDP (%)',range=[0, 5]),
                                              yaxis=dict(title='Researchers (in full-time equivalent) <br> per million inhabitants',range=[14, 8400]),
                                              paper_bgcolor='#f9f9f9',
                                              font=dict(size=12, color="#4d4d4d"),
                                              template='none'
                                              )

######################################################Accumulative########################################################

    filtered_by_year_and_country_df.sort_values(by=['GeoAreaName', 'TimePeriod'], inplace=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    color_numb4=0
    color_numb5 = 0
    fillmode='tonexty'
    for country in countries:
        fig.add_trace(
            go.Scatter(
                x=filtered_by_year_and_country_df['TimePeriod'][(filtered_by_year_and_country_df['SeriesDescription'] == 'International financial flows to developing countries in support of clean energy research and development and renewable energy production, including in hybrid systems (millions of constant 2016 United States dollars)')],
                y=filtered_by_year_and_country_df['Acc'][(filtered_by_year_and_country_df['SeriesDescription'] == 'International financial flows to developing countries in support of clean energy research and development and renewable energy production, including in hybrid systems (millions of constant 2016 United States dollars)') & (
                                        filtered_by_year_and_country_df['GeoAreaName'] == country)],
                fill=fillmode,
                name=country,
                mode='lines',
                fillcolor=color_accum[color_numb5],
                line_color=color_bar[color_numb5]


            ), secondary_y=False)
        color_numb5 += 1
        fillmode='tozeroy'

    for country in countries:
        fig.add_trace(
            go.Scatter(
                x=filtered_by_year_and_country_df['TimePeriod'][(filtered_by_year_and_country_df['SeriesDescription'] == 'International financial flows to developing countries in support of clean energy research and development and renewable energy production, including in hybrid systems (millions of constant 2016 United States dollars)')],
                y=filtered_by_year_and_country_df['Value'][
                    (filtered_by_year_and_country_df['SeriesDescription'] == 'Renewable energy share in the total final energy consumption (%)') & (
                                filtered_by_year_and_country_df['GeoAreaName'] == country)],
                # y=df['Value'][(df['SeriesDescription'] == 'Proportion of population with primary reliance on clean fuels and technology (%)') & (df['GeoAreaName']==country)]   ,
                name=country,
                line_color=color_line[color_numb4]

            ), secondary_y=True)
        color_numb4 += 1

    fig.update_layout(
        title=dict(text='Investiments accumulative and renewable energy share in final energy consumption',
                   x=0.5),
        yaxis=dict(title='Investiments accumulative <br> (millions of constant 2016 United States dollars)'),
        yaxis2=dict(title='Renewable energy share (%)', range=[0, 100]),
        xaxis=dict(title='Year'),
        paper_bgcolor='#f9f9f9',
        template='none',
        font=dict(size=12, color="#4d4d4d"),
        legend=dict(orientation='h', yanchor='top', xanchor='center', y=-0.3, x=0.5))

 ######################################################Dots########################################################
    codigo12 = ['Central and Southern Asia', 'Eastern and South-Eastern Asia', 'Europe and Northern America',
                'Latin America and the Caribbean','Northern Africa and Western Asia','Sub-Saharan Africa']
    policies = ['POLICY_ECONFIS', 'POLICY_MACRO', 'POLICY_REGLEG', 'POLICY_VOLSRG', "_T"]

    df.sort_values(by=['SeriesDescription','GeoAreaName','Policy instruments'], inplace=True)

    POLICY_ECONFIS = df['Value'][(df[
                                      'SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                                     df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == 'POLICY_ECONFIS')]
    POLICY_MACRO = df['Value'][(df[
                                    'SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                                   df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == 'POLICY_MACRO')]
    POLICY_REGLEG = df['Value'][(df[
                                     'SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                                    df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == 'POLICY_REGLEG')]
    POLICY_VOLSRG = df['Value'][(df[
                                     'SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                                    df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == 'POLICY_VOLSRG')]
    _T = df['Value'][(df[
                          'SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                         df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == '_T')]

    dots = go.Figure()

    dots.add_trace(go.Scatter(
        x=POLICY_ECONFIS,
        y=df['GeoAreaName'][(df['SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                                     df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == 'POLICY_ECONFIS')],
        name='Economic and fiscal instruments (taxes and tax <br> incentives, grants, preferential loans, etc.) ',
        marker=dict(
            color='rgba(165,0,38, 0.5)',
            line_color='rgba(165,0,38, 1.0)',
        )
    ))

    dots.add_trace(go.Scatter(
        x=POLICY_REGLEG,
        y=df['GeoAreaName'][(df['SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                                     df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == 'POLICY_REGLEG')],
        name='Regulatory and legal instruments (e.g. laws, <br> standards, enforcement measures)',
        marker=dict(
            color='rgba(244,109,67, 0.5)',
            line_color='rgba(244,109,67, 1.0)',
        )
    ))

    dots.add_trace(go.Scatter(
        x=POLICY_VOLSRG,
        y=df['GeoAreaName'][(df['SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                                     df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == 'POLICY_VOLSRG')],
        name='Voluntary and self-regulation schemes (e.g. sectoral <br> partnerships, codes of conduct, CSR initiatives)',
        marker=dict(
            color='rgba(116,173,209, 0.5)',
            line_color='rgba(116,173,209, 1.0)',
        )
    ))

    dots.add_trace(go.Scatter(
        x=_T,
        y=df['GeoAreaName'][(df['SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                                     df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == '_T')],
        name='No breakdown',
        marker=dict(
            color='rgba(5,48,97,0.5)',
            line_color='rgba(5,48,97, 1.0)',
        )
    ))

    dots.add_trace(go.Scatter(
        x=POLICY_MACRO,
        y=df['GeoAreaName'][(df['SeriesDescription'] == 'Countries with policy instrument for sustainable consumption and production (1 = YES; 0 = NO)') & (
                                     df['GeoAreaName'].isin(codigo12)) & (df['Policy instruments'] == 'POLICY_MACRO')],
        name='Macro policies (e.g. national strategies/action<br> plans, new institutions/entities)',
        marker=dict(
            color='rgba(27,120,55, 0.5)',
            line_color='rgba(27,120,55, 1.0)'
        )
    ))

    dots.update_traces(mode='markers', marker=dict(line_width=1, symbol='circle', size=10))

    dots.add_trace(go.Scatter(hovertemplate='%{x:.0} countries'))

    dots.update_layout(
        title="Indicator 12.1.1 - year 2019",
        hovermode="closest",
        yaxis=dict(gridwidth=1,
                   gridcolor="lightgray"),
        xaxis=dict(
            showgrid=True,
            showline=True,
            linecolor='black',
            tickfont_color='black',
            showticklabels=True,
            dtick=10,
            ticks='outside',
            tickcolor='black',
            zeroline=False,
            hoverformat='.0f'

        ),
        margin=dict(l=140, r=10, b=50, t=100),
        legend=dict(
            font_size=10,
            yanchor='bottom',
            xanchor='center',

        ),
        width=800,
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
######################################################Return########################################################

    return go.Figure(data=data_choropleth, layout=layout_choropleth), \
           go.Figure(data=data_choropleth2, layout=layout_choropleth2), \
           go.Figure(data=data_line1,layout=layout_line), \
           go.Figure(data=data_line_bar, layout=layout_line_bar), \
           go.Figure(data=data_bubble2, layout=layout_bubble2), \
           go.Figure(data=fig),\
           go.Figure(data=dots)

if __name__ == '__main__':
    app.run_server(debug=True)





