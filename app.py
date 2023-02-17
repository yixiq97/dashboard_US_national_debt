#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[8]:


import plotly.express as px 
import plotly.graph_objects as go


# In[30]:


import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


# ## Load data

# In[85]:


interest_df = pd.read_csv('interest.csv', header=0)
interest_spread_df = pd.read_csv('interest_spread.csv', header=0)
debt_main_df = pd.read_csv('debt_main.csv', header=0)
debt_ttl_df = pd.read_csv('debt_ttl.csv', header=0)
mts_mth_df = pd.read_csv('mts_mth.csv', header=0)
mts_yr_df = pd.read_csv('mts_yr.csv', header=0)



interest_spread_df['record_fiscal_year'] = mts_mth_df['record_fiscal_year']
debt_ttl_df['record_fiscal_year'] = mts_mth_df['record_fiscal_year']

# ## Create graphs

# In[67]:


print(len(interest_df),len(interest_spread_df),
      len(debt_main_df),len(debt_ttl_df),
      len(mts_mth_df),len(mts_yr_df))


# In[315]:


def debt_deficit_graph(mts_df,debt_df):
    fiscal_yr_ls = mts_df.record_fiscal_year.unique().tolist()
    fig = px.line(x = mts_df.current_month_dfct_sur_amt, y = debt_df.total_mil_amt,
                  color_discrete_sequence=['#696969']*len(fiscal_yr_ls),color = mts_mth_df.record_fiscal_year)
    fig.update_traces(line=dict(width=1.5))
    fig.update_layout(showlegend=False,yaxis_title="Debt amount",xaxis_title="Deficit amount")
    for fiscal_yr in fiscal_yr_ls:
        x_deficit = mts_df[mts_df['record_fiscal_year'] == fiscal_yr].current_month_dfct_sur_amt.tolist()[0]
        y_debt = debt_df[debt_df['record_fiscal_year'] == fiscal_yr].total_mil_amt.tolist()[0]
        fig.add_annotation(x=x_deficit, y=y_debt,
                           text=fiscal_yr,
                           font=dict(size=12,color='#696969'),
                           showarrow=False,
                           xshift=35,
                           yshift=5)

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black',gridwidth=0.1,gridcolor='#DCDCDC')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black',gridwidth=0.1,gridcolor='#DCDCDC')
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor':'rgba(0, 0, 0, 0)',})
    return fig

debt_deficit_fig = debt_deficit_graph(mts_mth_df,debt_ttl_df)



# In[418]:


def spread_deficit_graph(mts_df,spread_df):
    fig = go.Figure(data=[
    go.Bar(name="Accumulated deficit amount",
           x = mts_df.record_date,
           y = mts_df.current_month_dfct_sur_amt,
           marker_color = '#C0C0C0')#px.colors.qualitative.Set1[8])
    ])
    fig.add_trace(
        go.Scatter(name="Notes vs Bills", x = spread_df.record_date,
                   y = spread_df.notes_bills_spread,yaxis="y2",
                   marker_color = 'DarkTurquoise',#px.colors.sequential.Darkmint[-5],
                   line=dict(width=1.5))
    )
    fig.add_annotation(x=spread_df.record_date.tolist()[-1], y=list(spread_df.notes_bills_spread)[-1],xref="x",yref="y2",
                       text="Notes vs Bills",font=dict(size=12,color='DarkTurquoise'),showarrow=False,xshift=40,yshift=10)


    fig.add_trace(
        go.Scatter(name="Bonds vs Bills", x = spread_df.record_date,
                   y = spread_df.bonds_bills_spread,yaxis="y2",
                   marker_color = 'DarkTurquoise',#px.colors.sequential.Darkmint[-4],
                   line=dict(width=1.5)),
    )
    fig.add_annotation(x=spread_df.record_date.tolist()[-1], y=list(spread_df.bonds_bills_spread)[-1],xref="x",yref="y2",
                       text="Bonds vs Bills",font=dict(size=12,color='DarkTurquoise'),showarrow=False,xshift=40,yshift=10)

    fig.add_shape(type="line", xref="paper", yref="y2", x0=0, y0=0, x1=1, y1=0,
                  line=dict(color="Crimson",width=1.5),)

    fig.update_layout(
        showlegend=False,#legend=dict(orientation="h"),
        yaxis=dict(
            title=dict(text="Deficit amount"),
            side="right",
            range=[0, 3200000000000],
        ),
        yaxis2=dict(
            title=dict(text="Interest rate spread"),
            side="left",
            range=[-0.03, 0.05],
            overlaying="y",
        ),
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black',showgrid=False)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor':'rgba(0, 0, 0, 0)',})

    return fig
spread_deficit_fig = spread_deficit_graph(mts_mth_df,interest_spread_df)
#spread_deficit_fig.show()


# In[ ]:





# In[483]:


interest_fig = px.line(interest_df,
                       x="record_date", 
                       y="avg_interest_rate_amt", 
                       color_discrete_sequence=px.colors.sequential.Darkmint[-5:-1],#RdBu[-3:],
                       color='security_desc')
interest_fig.update_layout(legend=dict(orientation="h"),
                           legend_title_text='',
                           xaxis_showgrid=False, 
                           xaxis_title="",
                           yaxis_title="",
                           margin=dict(l=0, r=35,t=10,b=0),)
interest_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor':'rgba(0, 0, 0, 0)',})
#interest_fig.show()


# In[480]:


debt_fig = px.bar(debt_main_df,
                  x='record_date', 
                  y='total_mil_amt', 
                  color_discrete_sequence= px.colors.sequential.Darkmint[-5:-1],#RdBu[-3:],#px.colors.qualitative.T10,
                  color='security_class_desc')
debt_fig.update_layout(legend=dict(orientation="h"),
                       legend_title_text='',
                       xaxis_title="",
                       yaxis_title="",
                       margin=dict(l=0, r=35,t=10,b=0),)
debt_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor':'rgba(0, 0, 0, 0)',})
#debt_fig.show()


# In[445]:


rcpt_outly_fig = go.Figure(data=[
    go.Bar(name='Gross reception', 
           x = mts_yr_df.record_date, y = mts_yr_df.current_month_gross_rcpt_amt,
           marker_color = px.colors.sequential.RdBu[-2]),
    go.Bar(name='Gross outlay', 
           x = mts_yr_df.record_date, y = [-i for i in mts_yr_df.current_month_gross_outly_amt],
           marker_color = px.colors.sequential.RdBu[1])
])

rcpt_outly_fig.update_layout(legend=dict(orientation="h"),barmode='relative',margin=dict(l=10, r=35,t=10,b=0),)
rcpt_outly_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor':'rgba(0, 0, 0, 0)',})
#rcpt_outly_fig.show()


# In[446]:


deficit_fig = go.Figure(data=[
    go.Bar(name=" Monthly deficit/surplus",
           x = mts_mth_df.record_date, y = mts_mth_df.current_month_dfct_change_amt,
           marker_color = px.colors.sequential.RdBu[1]),
])
deficit_fig.add_trace(
    go.Scatter(name="Accumulated deficit", 
               x = mts_mth_df.record_date, y = mts_mth_df.current_month_dfct_sur_amt,
               marker_color = '#696969',line = dict(width=1.2))
)
deficit_fig.update_layout(legend=dict(orientation="h"),margin=dict(l=30, r=35,t=10,b=0),)
deficit_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor':'rgba(0, 0, 0, 0)',})
#deficit_fig.show()


# ## APP layout

# In[39]:


app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server


# In[519]:


#fiscal_yr_len = len(mts_mth_df.record_fiscal_year.unique())
#fiscal_yr_dict = dict(zip(range(fiscal_yr_len-1,-1,-1),fiscal_yr_val))
fiscal_yr_val = mts_mth_df.record_fiscal_year.unique().tolist()
fiscal_yr_val.insert(0,'All Fiscal Years')


# In[563]:


app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('U.S. Natinal Debt Dashboard',style={'fontSize':36,'color':'white','textAlign': 'center',"font-weight": "bold",'margin-left': '20px'}),
        ],className = 'navbar navbar-expand-lg navbar-dark bg-primary'),            
    ],style = {'margin-bottom':'50px'}),
    
    html.Div([
        html.Div([
            html.Div([
                html.P("National Debt Interest rate", className='card-header'),
                html.Div([
                    dcc.Graph(
                        id='interest-chart',figure = interest_fig
                    ),
                ],className='card-body',style={'width': '100%'})   
            ],className = 'card bg-light mb-3',style={'width': '96%','float': 'left'}),#style={'width': '48%','float': 'left','display': 'inline-block',}
            html.Div([
                html.P("National Debt Amount", className='card-header'),
                html.Div([
                    dcc.Graph(
                        id='debt-chart',figure = debt_fig
                    ),                        
                ],className='card-body'),
            ],className = 'card bg-light mb-3',style={'width': '96%','float': 'left'}), #style={'width': '48%','float': 'right','display': 'inline-block',}  
        ],style={'width': '23%','float': 'left','display': 'inline-block',}),
                
        html.Div([
            html.Div([
                html.P("Receipts and Outlays of the Government", className='card-header'),
                html.Div([
                    dcc.Graph(
                        id='rcpt-outly-chart',figure = rcpt_outly_fig
                    ),                        
                ],className='card-body'),
            ],className = 'card bg-light mb-3',style={'width': '96%','float': 'right'}),#style={'width': '48%','float': 'left','display': 'inline-block',}
            html.Div([
                html.P("Deficit of the Government", className='card-header'),
                html.Div([
                    dcc.Graph(
                        id='deficit-chart',figure = deficit_fig
                    ),                                        
                ],className='card-body'),
            ],className = 'card bg-light mb-3',style={'width': '96%','float': 'right'}), #style={'width': '48%','float': 'right','display': 'inline-block',}                   
        ],style={'width': '23%','float': 'right','display': 'inline-block',}),
        
        html.Div([
            html.P("Government Deficit & National Debt", className='card-header'),
            html.Div([
                html.Div([
                    html.Label("Select the Fiscal Year", className='form-label mt-4'),
                    dcc.Dropdown(
                        id="fiscal-yr-filter",
                        options=[
                            {"label": fiscal_yr, "value": fiscal_yr}
                            for fiscal_yr in fiscal_yr_val
                        ],
                        #multi=True,
                        clearable=False,
                    ),
                ], className="form-group"),
                dcc.Graph(
                    id='spread-deficit-chart',figure = spread_deficit_fig
                ),    
                dcc.Graph(
                    id='debt-deficit-chart',figure = debt_deficit_fig
                ),    
            ],style={'width': '98%','float': 'right','display': 'inline-block'},className='card-body'),
        ],className = 'card border-primary mb-3',
        style={'width': '54%','float': 'right','display': 'inline-block',}),           
        
    ],style={'width': '97%','float': 'right','margin-right': '20px','margin-left': '20px',}),    
])


# In[566]:


@app.callback(
    [Output('spread-deficit-chart', 'figure'),Output('debt-deficit-chart', 'figure')],
    Input('fiscal-yr-filter', 'value'))
def update_output(fiscal_yr):
    if fiscal_yr == fiscal_yr_val[0]:
        spread_deficit_fig = spread_deficit_graph(mts_mth_df, interest_spread_df)
        debt_deficit_fig = debt_deficit_graph(mts_mth_df, debt_ttl_df)
    else:
        spread_deficit_fig = spread_deficit_graph(mts_mth_df, interest_spread_df)
        fiscal_yr_date = mts_mth_df[mts_mth_df['record_fiscal_year'] == fiscal_yr].record_date.tolist()
        spread_deficit_fig.add_vrect(
            x0=fiscal_yr_date[-1],
            x1=fiscal_yr_date[0],
            fillcolor="LightCoral", opacity=0.3,
            layer="below", line_width=0,
        )

        debt_deficit_fig = debt_deficit_graph(mts_mth_df, debt_ttl_df)
        debt_deficit_fig.add_trace(go.Scatter(
            x=mts_mth_df[mts_mth_df['record_fiscal_year'] == fiscal_yr].current_month_dfct_sur_amt,
            y=debt_ttl_df[debt_ttl_df['record_fiscal_year'] == fiscal_yr].total_mil_amt,
            marker_color='LightCoral'
        ))
        debt_deficit_fig.add_annotation(x=mts_mth_df[mts_mth_df['record_fiscal_year'] == fiscal_yr].current_month_dfct_sur_amt.tolist()[0],
                                        y=debt_ttl_df[debt_ttl_df['record_fiscal_year'] == fiscal_yr].total_mil_amt.tolist()[0],
                                        text=fiscal_yr,
                                        font=dict(size=12,color='LightCoral'),
                                        showarrow=False,
                                        xshift=35,
                                        yshift=5)

    '''
    mts_df = mts_mth_df[mts_mth_df['record_fiscal_year'] == fiscal_yr]
    spread_df = interest_spread_df[interest_spread_df['record_fiscal_year'] == fiscal_yr]
    spread_deficit_fig = spread_deficit_graph(mts_df, spread_df)
    '''
    
    return spread_deficit_fig,debt_deficit_fig


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




